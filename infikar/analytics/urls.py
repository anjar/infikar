from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Analytics dashboard
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
]
