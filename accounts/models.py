from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """Custom User model with additional fields for bio sites"""
    
    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('pro_trial', 'Pro Trial'),
    ]
    
    # Username validation - only alphanumeric, ., -, _
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._-]+$',
        message='Username can only contain letters, numbers, dots, hyphens, and underscores.'
    )
    
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator],
        help_text='Required. 30 characters or fewer. Letters, numbers, dots, hyphens, and underscores only.'
    )
    
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    subscription_tier = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_CHOICES,
        default='free'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    
    # Profile information
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return f"@{self.username}"
    
    @property
    def is_pro_user(self):
        """Check if user has active pro subscription"""
        if self.subscription_tier == 'pro':
            return True
        elif self.subscription_tier == 'pro_trial':
            return self.trial_end_date and self.trial_end_date > timezone.now()
        return False
    
    @property
    def subscription_status(self):
        """Get current subscription status"""
        if self.subscription_tier == 'free':
            return 'free'
        elif self.subscription_tier == 'pro_trial':
            if self.trial_end_date and self.trial_end_date > timezone.now():
                return 'trial'
            else:
                return 'trial_expired'
        elif self.subscription_tier == 'pro':
            if self.subscription_end_date and self.subscription_end_date > timezone.now():
                return 'active'
            else:
                return 'expired'
        return 'free'
    
    def get_card_limit(self):
        """Get card limit based on subscription"""
        if self.is_pro_user:
            from django.conf import settings
            return settings.PRO_CARD_LIMIT
        return 10  # Free limit
    
    def get_social_links_limit(self):
        """Get social links limit based on subscription"""
        if self.is_pro_user:
            from django.conf import settings
            return settings.PRO_SOCIAL_LINKS
        return 5  # Free limit
    
    def get_picks_limit(self):
        """Get picks limit based on subscription"""
        if self.is_pro_user:
            from django.conf import settings
            return settings.PRO_PICKS_LIMIT
        return 50  # Free limit


class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Social media links
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    github = models.URLField(blank=True)
    discord = models.URLField(blank=True)
    twitch = models.URLField(blank=True)
    
    # Analytics settings
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_social_links(self):
        """Get all non-empty social links"""
        social_fields = [
            'website', 'twitter', 'instagram', 'linkedin', 
            'youtube', 'tiktok', 'facebook', 'github', 
            'discord', 'twitch'
        ]
        return {field: getattr(self, field) for field in social_fields if getattr(self, field)}
