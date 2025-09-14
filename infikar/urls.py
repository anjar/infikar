"""
URL configuration for infikar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from infikar.health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Health check
    path("health/", health_check, name="health_check"),
    
    # Authentication URLs
    path("auth/", include("infikar.accounts.urls")),
    
    # Public URLs (home and user profiles)
    path("", include("infikar.cards.urls")),
    
    # App URLs (dashboard and cards)
    path("app/", include("infikar.cards.app_urls")),
    
    # Analytics and subscriptions
    path("analytics/", include("infikar.analytics.urls")),
    path("subscriptions/", include("infikar.subscriptions.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
