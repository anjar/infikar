from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class OnboardMiddleware:
    """
    Middleware to redirect users without usernames to onboard page.
    Users can only access: login, logout, onboard, and public pages.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for certain paths
        if self._should_skip_middleware(request):
            return self.get_response(request)
        
        # Check if user is authenticated and has no username
        if (request.user.is_authenticated and 
            hasattr(request.user, 'username') and 
            not request.user.username):
            
            # Only redirect if not already on onboard page
            if not request.path.startswith('/app/onboard/'):
                return redirect('accounts:onboard')
        
        return self.get_response(request)
    
    def _should_skip_middleware(self, request):
        """Check if middleware should be skipped for this request"""
        path = request.path
        
        # Skip for static files, admin, and API endpoints
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/health/',
            '/favicon.ico',
        ]
        
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return True
        
        # Skip for public pages (home, user profiles, card details)
        if path in ['/', '/app/signup/', '/app/login/', '/app/logout/', '/app/onboard/']:
            return True
        
        # Skip for user profile pages (@username)
        if path.startswith('/@') and '/' not in path[2:]:
            return True
        
        # Skip for card detail pages (@username/card-slug)
        if path.startswith('/@') and path.count('/') == 2:
            return True
        
        # Skip for AJAX requests (including username check)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
        
        # Skip for API endpoints
        if path.startswith('/app/check-username/'):
            return True
        
        return False
