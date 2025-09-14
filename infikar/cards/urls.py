from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    # Public URLs
    path('', views.HomeView.as_view(), name='home'),
    path('@<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('@<str:username>/<str:card_slug>/', views.CardDetailView.as_view(), name='card_detail'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
