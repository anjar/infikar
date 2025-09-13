from django.contrib import admin
from .models import CardTemplate, Card, LinkContent, AboutContent, RecommendationContent, RecommendationPick, SplashContent, YouTubeContent, YouTubeVideo


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_premium', 'sort_order')
    list_filter = ('is_active', 'is_premium')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'card_type', 'is_published', 'is_draft', 'is_hidden', 'created_at')
    list_filter = ('card_type', 'is_published', 'is_draft', 'is_hidden', 'created_at')
    search_fields = ('title', 'user__username', 'user__email')
    ordering = ('-created_at',)


@admin.register(LinkContent)
class LinkContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'card', 'url', 'is_email', 'is_phone')
    list_filter = ('is_email', 'is_phone', 'created_at')
    search_fields = ('title', 'url', 'card__title')


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('heading', 'card', 'created_at')
    search_fields = ('heading', 'card__title')


@admin.register(RecommendationContent)
class RecommendationContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'card', 'created_at')
    search_fields = ('title', 'card__title')


@admin.register(RecommendationPick)
class RecommendationPickAdmin(admin.ModelAdmin):
    list_display = ('title', 'recommendation', 'order_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'recommendation__title')


@admin.register(SplashContent)
class SplashContentAdmin(admin.ModelAdmin):
    list_display = ('heading', 'card', 'created_at')
    search_fields = ('heading', 'card__title')


@admin.register(YouTubeContent)
class YouTubeContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'card', 'channel_url', 'button_label')
    search_fields = ('title', 'channel_url', 'card__title')


@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_content', 'video_url', 'published_at')
    list_filter = ('published_at', 'created_at')
    search_fields = ('title', 'video_url')
