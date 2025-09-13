from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'subscription_tier', 'is_active')
    list_filter = ('subscription_tier', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Subscription Info', {'fields': ('subscription_tier', 'subscription_start_date', 'subscription_end_date', 'trial_end_date')}),
        ('Profile Info', {'fields': ('bio', 'avatar')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'twitter', 'instagram', 'youtube')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
