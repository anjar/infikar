from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, UserProfile
import json


class CustomSignupView(TemplateView):
    """Custom signup view with email/password and social login"""
    template_name = 'accounts/signup.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to dashboard
        if request.user.is_authenticated:
            if not request.user.username:
                return redirect('accounts:onboard')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignupForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Activate immediately for demo
            user.username = None  # Set username to None initially
            user.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Log user in
            login(request, user)
            
            # Send email verification (you can implement this later)
            # send_verification_email(user)
            
            messages.success(request, 'Account created! Please choose your username.')
            return redirect('accounts:onboard')
        
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class OnboardView(TemplateView):
    """Username setup after registration"""
    template_name = 'accounts/username_setup.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect unauthenticated users to login
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        # Redirect users who already have username to dashboard
        if request.user.username:
            return redirect('accounts:dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        username = request.POST.get('username', '').strip()
        
        if not username:
            messages.error(request, 'Username is required')
            return self.get(request, *args, **kwargs)
        
        # Check if username is available
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return self.get(request, *args, **kwargs)
        
        # Update user with username
        user.username = username
        user.is_active = True  # Activate user after username setup
        user.save()
        
        # Clear onboard session
        if 'onboard_user_id' in request.session:
            del request.session['onboard_user_id']
        
        messages.success(request, f'Welcome to Infikar, @{username}!')
        return redirect('accounts:dashboard')


class CustomLoginView(LoginView):
    """Custom login view with email/password and social login"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to appropriate page
        if request.user.is_authenticated:
            if not request.user.username:
                return redirect('accounts:onboard')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        # Check if user has username after login
        if not self.request.user.username:
            return reverse_lazy('accounts:onboard')
        return reverse_lazy('accounts:dashboard')


class DashboardView(TemplateView):
    """User dashboard for creating/managing cards"""
    template_name = 'accounts/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect unauthenticated users to login
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        # Redirect users without username to onboard
        if not request.user.username:
            return redirect('accounts:onboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['cards'] = user.cards.all().order_by('-created_at')
        context['card_count'] = user.cards.count()
        context['card_limit'] = user.get_card_limit()
        return context


@require_http_methods(["POST"])
def check_username_availability(request):
    """AJAX endpoint to check username availability with rate limiting"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        if not username:
            return JsonResponse({'available': False, 'message': 'Username is required'})
        
        # Basic rate limiting - check if too many requests in short time
        # You can enhance this with Redis-based rate limiting later
        from .username_rules import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH
        if len(username) < MIN_USERNAME_LENGTH:
            return JsonResponse({'available': False, 'message': f'Username must be at least {MIN_USERNAME_LENGTH} characters'})
        
        if len(username) > MAX_USERNAME_LENGTH:
            return JsonResponse({'available': False, 'message': f'Username must be {MAX_USERNAME_LENGTH} characters or less'})
        
        # Check if username is available
        if User.objects.filter(username=username).exists():
            return JsonResponse({'available': False, 'message': 'Username is already taken'})
        
        # Check username validation
        from .validators import validate_username
        try:
            validate_username(username)
            return JsonResponse({'available': True, 'message': 'Username is available'})
        except forms.ValidationError as e:
            return JsonResponse({'available': False, 'message': str(e)})
            
    except json.JSONDecodeError:
        return JsonResponse({'available': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'available': False, 'message': 'Invalid request'})


class SignupForm(forms.ModelForm):
    """Custom signup form with email and password"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        min_length=8
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
