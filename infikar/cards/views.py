from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Card, CardTemplate, LinkContent
from .forms import CardCreateForm, LinkCreateForm

User = get_user_model()


class HomeView(TemplateView):
    template_name = 'cards/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_users'] = User.objects.filter(is_active=True)[:6]
        context['templates'] = CardTemplate.objects.filter(is_active=True)[:5]
        return context


class UserProfileView(DetailView):
    model = User
    template_name = "cards/user_profile.html"
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['cards'] = Card.objects.filter(
            user=user, 
            is_published=True, 
            is_hidden=False
        ).order_by('sort_order')
        return context


class CardDetailView(DetailView):
    model = Card
    template_name = "cards/card_detail.html"
    context_object_name = 'card'
    
    def get_object(self):
        username = self.kwargs['username']
        card_slug = self.kwargs['card_slug']
        return Card.objects.get(
            user__username=username,
            slug=card_slug,
            is_published=True
        )


class DashboardView(TemplateView):
    """User dashboard for creating/managing cards"""
    template_name = 'cards/dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['cards'] = user.cards.all().order_by('-created_at')
        context['card_count'] = user.cards.count()
        context['card_limit'] = user.get_card_limit()
        return context


class CardCreateView(TemplateView):
    """Create a new card with dynamic form handling"""
    template_name = 'cards/card_create.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = CardTemplate.objects.filter(is_active=True)
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle the new form structure
        action = request.POST.get('action', 'publish')
        card_type = request.POST.get('card_type')
        
        if action == 'preview':
            return self.preview_card(request)
        elif card_type == 'link':
            return self.create_link_collection(request)
        else:
            # For other card types, use the old form
            form = CardCreateForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.template = CardTemplate.objects.first()
                form.save()
                messages.success(request, f'Card "{form.instance.title}" created successfully!')
                return redirect('app:dashboard')
            else:
                return self.form_invalid(form)
    
    def preview_card(self, request):
        """Preview card without saving to database"""
        card_type = request.POST.get('card_type')
        
        if card_type == 'link':
            # Create a temporary card object for preview
            card_data = {
                'title': request.POST.get('title', 'Preview Card'),
                'card_type': 'link',
                'template_id': request.POST.get('template'),
                'is_published': False,
                'is_draft': True,
                'user': request.user
            }
            
            # Create temporary card for preview
            temp_card = Card(**card_data)
            temp_card.id = 0  # Temporary ID for preview
            
            # Add links data
            links_data = self.extract_links_data(request.POST, request.FILES)
            temp_card._preview_links = links_data
            
            # Add social media data
            social_data = self.extract_social_data(request.POST)
            temp_card.social_links = social_data
            
            context = {
                'card': temp_card,
                'is_preview': True,
                'templates': CardTemplate.objects.filter(is_active=True)
            }
            return render(request, 'cards/card_preview.html', context)
        
        return redirect('cards:create')
    
    def create_link_collection(self, request):
        """Create a link collection card with links and social media"""
        try:
            action = request.POST.get('action', 'publish')
            is_published = action == 'publish'
            
            # Create the card
            card = Card.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                card_type='link',
                template_id=request.POST.get('template'),
                is_published=is_published,
                is_draft=not is_published
            )
            
            # Handle card image upload
            if 'card_image' in request.FILES:
                card.card_image = request.FILES['card_image']
                card.save()
            
            # Create links
            links_data = self.extract_links_data(request.POST, request.FILES)
            for link_data in links_data:
                if link_data.get('title') and link_data.get('url'):
                    LinkContent.objects.create(
                        card=card,
                        title=link_data['title'],
                        url=link_data['url'],
                        link_text=link_data.get('link_text', ''),
                        description=link_data.get('description', ''),
                        sort_order=len(card.link_contents.all())
                    )
            
            # Create social media links (stored in card's social_links JSON field)
            social_data = self.extract_social_data(request.POST)
            if social_data:
                card.social_links = social_data
                card.save()
            
            action_text = "published" if is_published else "saved as draft"
            messages.success(request, f'Link collection "{card.title}" {action_text} successfully!')
            return redirect('app:manage', card_id=card.id)
            
        except Exception as e:
            messages.error(request, f'Error creating card: {str(e)}')
            return redirect('app:create')
    
    def extract_links_data(self, post_data, files_data=None):
        """Extract links data from POST request and files"""
        links = []
        i = 1
        while f'links[{i}][title]' in post_data:
            link_data = {
                'title': post_data.get(f'links[{i}][title]', ''),
                'url': post_data.get(f'links[{i}][url]', ''),
                'link_text': post_data.get(f'links[{i}][link_text]', ''),
                'description': post_data.get(f'links[{i}][description]', ''),
            }
            if files_data and f'links[{i}][image]' in files_data:
                link_data['image'] = files_data[f'links[{i}][image]']
            if link_data['title'] and link_data['url']:
                links.append(link_data)
            i += 1
        return links
    
    def extract_social_data(self, post_data):
        """Extract social media data from POST request"""
        social_links = {}
        i = 1
        while f'social[{i}][platform]' in post_data:
            platform = post_data.get(f'social[{i}][platform]', '')
            url = post_data.get(f'social[{i}][url]', '')
            text = post_data.get(f'social[{i}][text]', '')
            
            if platform and url:
                social_links[platform] = {
                    'url': url,
                    'text': text or platform.title()
                }
            i += 1
        return social_links
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = CardTemplate.objects.filter(is_active=True)
        return context


class CardManageView(TemplateView):
    """Manage card content - links, etc."""
    template_name = 'cards/card_manage.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_id = self.kwargs['card_id']
        card = get_object_or_404(Card, id=card_id, user=self.request.user)
        
        context['card'] = card
        context['links'] = card.link_contents.all().order_by('sort_order')
        context['link_count'] = card.link_contents.count()
        context['link_limit'] = 100  # Free user limit
        context['is_pro'] = self.request.user.is_staff  # Simple pro check for now
        
        return context
    
    def post(self, request, card_id):
        """Handle AJAX requests for social media updates"""
        try:
            import json
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'update_social':
                card = get_object_or_404(Card, id=card_id, user=request.user)
                social_links = data.get('social_links', {})
                card.social_links = social_links
                card.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class LinkCreateView(CreateView):
    """Create a new link for a card"""
    model = LinkContent
    form_class = LinkCreateForm
    template_name = 'cards/link_form.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_card(self):
        return get_object_or_404(Card, id=self.kwargs['card_id'], user=self.request.user)
    
    def form_valid(self, form):
        card = self.get_card()
        
        # Check link limit
        if card.link_contents.count() >= 100:  # Free user limit
            messages.error(self.request, 'You have reached the maximum number of links (100)')
            return redirect('app:manage', card_id=card.id)
        
        form.instance.card = card
        form.instance.sort_order = card.link_contents.count()
        response = super().form_valid(form)
        messages.success(self.request, f'Link "{form.instance.title}" added successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('cards:manage', kwargs={'card_id': self.kwargs['card_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card'] = self.get_card()
        context['action'] = 'Add'
        return context


class LinkUpdateView(UpdateView):
    """Update an existing link"""
    model = LinkContent
    form_class = LinkCreateForm
    template_name = 'cards/link_form.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return LinkContent.objects.filter(card__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('cards:manage', kwargs={'card_id': self.object.card.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card'] = self.object.card
        context['action'] = 'Edit'
        return context


class LinkDeleteView(DeleteView):
    """Delete a link"""
    model = LinkContent
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return LinkContent.objects.filter(card__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('cards:manage', kwargs={'card_id': self.object.card.id})
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Link "{self.object.title}" deleted successfully!')
        return response


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LinkReorderView(TemplateView):
    """Handle drag-and-drop reordering of links"""
    
    def post(self, request, card_id):
        try:
            card = get_object_or_404(Card, id=card_id, user=request.user)
            data = json.loads(request.body)
            link_orders = data.get('link_orders', [])
            
            # Update sort orders
            for item in link_orders:
                link_id = item.get('id')
                sort_order = item.get('order')
                if link_id and sort_order is not None:
                    LinkContent.objects.filter(
                        id=link_id, 
                        card=card
                    ).update(sort_order=sort_order)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@method_decorator(login_required, name='dispatch')
class CardPublishView(TemplateView):
    """Publish or save as draft"""
    
    def post(self, request, card_id):
        card = get_object_or_404(Card, id=card_id, user=request.user)
        action = request.POST.get('action')
        
        if action == 'publish':
            card.is_published = True
            card.is_draft = False
            card.save()
            messages.success(request, f'Card "{card.title}" published successfully!')
        elif action == 'draft':
            if request.user.is_staff:  # Pro users can save as draft
                card.is_published = False
                card.is_draft = True
                card.save()
                messages.success(request, f'Card "{card.title}" saved as draft!')
            else:
                messages.error(request, 'Draft feature is only available for Pro users')
        
        return redirect('cards:manage', card_id=card.id)