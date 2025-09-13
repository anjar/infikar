from django.shortcuts import render
from django.views.generic import TemplateView

class AnalyticsDashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'