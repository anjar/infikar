from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Subscription plans
    path('', views.PlanListView.as_view(), name='plan_list'),
]
