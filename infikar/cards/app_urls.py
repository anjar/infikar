from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Card Management
    path('cards/create/', views.CardCreateView.as_view(), name='create'),
    path('cards/manage/<int:card_id>/', views.CardManageView.as_view(), name='manage'),
    path('cards/manage/<int:card_id>/publish/', views.CardPublishView.as_view(), name='publish'),
    
    # Link Management
    path('cards/manage/<int:card_id>/links/add/', views.LinkCreateView.as_view(), name='link_add'),
    path('cards/links/<int:pk>/edit/', views.LinkUpdateView.as_view(), name='link_edit'),
    path('cards/links/<int:pk>/delete/', views.LinkDeleteView.as_view(), name='link_delete'),
    path('cards/manage/<int:card_id>/links/reorder/', views.LinkReorderView.as_view(), name='link_reorder'),
]
