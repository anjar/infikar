from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()


class CardTemplate(models.Model):
    """Template for card styling"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Template styling
    font_family = models.CharField(max_length=100, default='Inter')
    font_weights = models.JSONField(default=list)  # Available font weights
    color_scheme = models.JSONField(default=dict)  # Color palette
    background_image = models.ImageField(upload_to='templates/', blank=True, null=True)
    preview_image = models.ImageField(upload_to='templates/previews/', blank=True, null=True)
    
    # Template settings
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Card(models.Model):
    """Main card model for bio sites"""
    
    CARD_TYPES = [
        ('link', 'Link Collection'),
        ('about', 'About'),
        ('recommendation', 'Recommendation/Top Picks'),
        ('splash', 'Splash'),
        ('youtube', 'YouTube Channel'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    template = models.ForeignKey(CardTemplate, on_delete=models.CASCADE, related_name='cards')
    
    # Card settings
    is_published = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    
    # Custom styling
    custom_font_family = models.CharField(max_length=100, blank=True)
    custom_font_weight = models.CharField(max_length=20, blank=True)
    custom_font_size = models.PositiveIntegerField(default=16, validators=[MinValueValidator(8), MaxValueValidator(72)])
    custom_text_transform = models.CharField(max_length=20, choices=[
        ('none', 'None'),
        ('uppercase', 'Uppercase'),
        ('lowercase', 'Lowercase'),
        ('capitalize', 'Capitalize'),
    ], default='none')
    custom_background_color = models.CharField(max_length=7, default='#ffffff')  # Hex color
    
    # Social media links (JSON field for flexibility)
    social_links = models.JSONField(default=dict, blank=True)
    
    # Card image override
    card_image = models.ImageField(upload_to='cards/card_images/', blank=True, null=True)
    
    # Ordering
    sort_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'slug']
        ordering = ['sort_order', 'created_at']
    
    def __str__(self):
        return f"{self.user.username}/{self.slug}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('card_detail', kwargs={'username': self.user.username, 'card_slug': self.slug})
    
    def get_preview_url(self):
        return reverse('card_preview', kwargs={'username': self.user.username, 'card_slug': self.slug})


class CardContent(models.Model):
    """Base content model for different card types"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='contents')
    
    # Common fields
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cards/images/', blank=True, null=True)
    
    # Ordering
    sort_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['sort_order', 'created_at']


class LinkContent(CardContent):
    """Content for link collection cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='link_contents')
    url = models.URLField()
    link_text = models.CharField(max_length=100, blank=True)
    is_email = models.BooleanField(default=False)
    is_phone = models.BooleanField(default=False)
    
    # Auto-fetch settings
    auto_fetch_title = models.BooleanField(default=True)
    auto_fetch_description = models.BooleanField(default=True)
    auto_fetch_image = models.BooleanField(default=True)
    
    # Fetched data (cached)
    fetched_title = models.CharField(max_length=200, blank=True)
    fetched_description = models.TextField(blank=True)
    fetched_image_url = models.URLField(blank=True)
    last_fetched = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.card.title} - {self.title}"


class AboutContent(CardContent):
    """Content for about cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='about_contents')
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(max_length=500)
    
    # Single link
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)
    
    # Social media links (JSON field for flexibility)
    social_links = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.card.title} - {self.heading}"


class RecommendationContent(CardContent):
    """Content for recommendation/top picks cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='recommendation_contents')
    subscription_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.card.title} - {self.title}"


class RecommendationPick(models.Model):
    """Individual picks within recommendation cards"""
    recommendation = models.ForeignKey(RecommendationContent, on_delete=models.CASCADE, related_name='picks')
    
    order_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cards/picks/', blank=True, null=True)
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_number']
    
    def __str__(self):
        return f"{self.recommendation.title} - Pick #{self.order_number}"


class SplashContent(CardContent):
    """Content for splash cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='splash_contents')
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=200, blank=True)
    
    # Single link
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)
    
    # Social media links
    social_links = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.card.title} - {self.heading}"


class YouTubeContent(CardContent):
    """Content for YouTube channel cards"""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='youtube_contents')
    channel_url = models.URLField()
    button_label = models.CharField(max_length=50, default='Subscribe')
    
    # YouTube videos
    max_videos = models.PositiveIntegerField(default=100)
    auto_fetch_videos = models.BooleanField(default=False)
    last_video_fetch = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.card.title} - YouTube Channel"


class YouTubeVideo(models.Model):
    """Individual YouTube videos"""
    youtube_content = models.ForeignKey(YouTubeContent, on_delete=models.CASCADE, related_name='videos')
    
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    duration = models.CharField(max_length=20, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Ordering
    sort_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-published_at']
    
    def __str__(self):
        return f"{self.youtube_content.title} - {self.title}"
