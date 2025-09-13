from django.shortcuts import render
from django.views.generic import TemplateView

class PlanListView(TemplateView):
    template_name = 'subscriptions/plan_list.html'