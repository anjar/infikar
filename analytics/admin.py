from django.contrib import admin
from .models import AnalyticsEvent, CardAnalytics, UserAnalytics, DailyAnalytics


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'content_object', 'user', 'ip_address', 'country', 'created_at')
    list_filter = ('event_type', 'country', 'device_type', 'created_at')
    search_fields = ('ip_address', 'user__username', 'user__email')
    ordering = ('-created_at',)


@admin.register(CardAnalytics)
class CardAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('card', 'total_views', 'total_clicks', 'views_7_days', 'clicks_7_days', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('card__title', 'card__user__username')


@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_views', 'total_clicks', 'views_7_days', 'clicks_7_days', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('user__username', 'user__email')


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('card', 'date', 'views', 'clicks', 'new_users', 'returning_users')
    list_filter = ('date', 'card__user')
    search_fields = ('card__title', 'card__user__username')
    ordering = ('-date',)
