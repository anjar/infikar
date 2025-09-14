from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='cards:home'), name='logout'),
    
    # Onboard
    path('onboard/', views.OnboardView.as_view(), name='onboard'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # AJAX endpoints
    path('check-username/', views.check_username_availability, name='check_username'),
]
