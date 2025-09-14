from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Card, CardTemplate

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