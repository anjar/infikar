from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class AnalyticsEvent(models.Model):
    """Track various analytics events"""
    
    EVENT_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('impression', 'Impression'),
        ('conversion', 'Conversion'),
    ]
    
    # Generic foreign key to track any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Event details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Request details
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True)
    
    # Location data
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Device/browser info
    device_type = models.CharField(max_length=50, blank=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.content_object}"


class CardAnalytics(models.Model):
    """Aggregated analytics for cards"""
    card = models.OneToOneField('cards.Card', on_delete=models.CASCADE, related_name='analytics')
    
    # View counts
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    
    # Click counts
    total_clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    
    # Time-based metrics
    views_7_days = models.PositiveIntegerField(default=0)
    views_30_days = models.PositiveIntegerField(default=0)
    clicks_7_days = models.PositiveIntegerField(default=0)
    clicks_30_days = models.PositiveIntegerField(default=0)
    
    # Geographic data (JSON fields for flexibility)
    top_countries = models.JSONField(default=list)
    top_cities = models.JSONField(default=list)
    
    # Traffic sources
    top_referrers = models.JSONField(default=list)
    direct_traffic = models.PositiveIntegerField(default=0)
    social_traffic = models.PositiveIntegerField(default=0)
    search_traffic = models.PositiveIntegerField(default=0)
    
    # User behavior
    new_vs_returning = models.JSONField(default=dict)
    avg_time_on_page = models.FloatField(default=0.0)  # in seconds
    
    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.card}"
    
    def get_click_through_rate(self):
        """Calculate click-through rate"""
        if self.total_views > 0:
            return (self.total_clicks / self.total_views) * 100
        return 0.0
    
    def get_top_traffic_source(self):
        """Get the top traffic source"""
        sources = {
            'direct': self.direct_traffic,
            'social': self.social_traffic,
            'search': self.search_traffic,
        }
        if self.top_referrers:
            sources['referrer'] = max(self.top_referrers, key=lambda x: x.get('count', 0)).get('count', 0)
        
        return max(sources, key=sources.get) if any(sources.values()) else 'direct'


class UserAnalytics(models.Model):
    """Aggregated analytics for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    
    # Overall stats
    total_views = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    
    # Time-based metrics
    views_7_days = models.PositiveIntegerField(default=0)
    views_30_days = models.PositiveIntegerField(default=0)
    clicks_7_days = models.PositiveIntegerField(default=0)
    clicks_30_days = models.PositiveIntegerField(default=0)
    
    # Geographic data
    top_countries = models.JSONField(default=list)
    top_cities = models.JSONField(default=list)
    
    # Traffic sources
    top_referrers = models.JSONField(default=list)
    direct_traffic = models.PositiveIntegerField(default=0)
    social_traffic = models.PositiveIntegerField(default=0)
    search_traffic = models.PositiveIntegerField(default=0)
    
    # User behavior
    new_vs_returning = models.JSONField(default=dict)
    
    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.user.username}"


class DailyAnalytics(models.Model):
    """Daily aggregated analytics for cards"""
    card = models.ForeignKey('cards.Card', on_delete=models.CASCADE, related_name='daily_analytics')
    date = models.DateField()
    
    # Daily metrics
    views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    
    # Geographic data
    countries = models.JSONField(default=dict)
    cities = models.JSONField(default=dict)
    
    # Traffic sources
    referrers = models.JSONField(default=dict)
    direct_traffic = models.PositiveIntegerField(default=0)
    social_traffic = models.PositiveIntegerField(default=0)
    search_traffic = models.PositiveIntegerField(default=0)
    
    # User behavior
    new_users = models.PositiveIntegerField(default=0)
    returning_users = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['card', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.card} - {self.date}"
