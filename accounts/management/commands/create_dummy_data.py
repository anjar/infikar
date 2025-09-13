from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import UserProfile
from cards.models import (
    CardTemplate, Card, LinkContent, AboutContent, 
    RecommendationContent, RecommendationPick, SplashContent, 
    YouTubeContent, YouTubeVideo
)
from subscriptions.models import SubscriptionPlan
import random
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Create dummy data for testing the Infikar platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--cards-per-user',
            type=int,
            default=5,
            help='Number of cards per user (default: 5)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎨 Creating dummy data for Infikar...'))
        
        # Create subscription plans
        self.create_subscription_plans()
        
        # Create card templates
        self.create_card_templates()
        
        # Create users and their content
        num_users = options['users']
        cards_per_user = options['cards_per_user']
        
        for i in range(num_users):
            user = self.create_user(i)
            self.create_user_profile(user)
            self.create_user_cards(user, cards_per_user)
            
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created {num_users} users with {cards_per_user} cards each!')
        )
        self.stdout.write(
            self.style.SUCCESS('🌐 Visit http://localhost:8000/admin to see the data')
        )

    def create_subscription_plans(self):
        """Create subscription plans"""
        plans = [
            {
                'name': 'Free Plan',
                'plan_type': 'free',
                'billing_cycle': None,
                'price_monthly': None,
                'price_yearly': None,
                'card_limit': 10,
                'social_links_limit': 5,
                'picks_limit': 50,
                'can_save_drafts': False,
                'can_hide_cards': False,
                'has_analytics': False,
                'has_google_analytics': False,
                'has_custom_templates': False,
                'has_auto_fetch': True,
                'has_youtube_api': False,
                'trial_days': 0,
                'is_active': True,
                'is_popular': False,
            },
            {
                'name': 'Pro Monthly',
                'plan_type': 'pro',
                'billing_cycle': 'monthly',
                'price_monthly': 9.99,
                'price_yearly': None,
                'card_limit': 50,
                'social_links_limit': 15,
                'picks_limit': 200,
                'can_save_drafts': True,
                'can_hide_cards': True,
                'has_analytics': True,
                'has_google_analytics': True,
                'has_custom_templates': True,
                'has_auto_fetch': True,
                'has_youtube_api': True,
                'trial_days': 7,
                'is_active': True,
                'is_popular': True,
            },
            {
                'name': 'Pro Yearly',
                'plan_type': 'pro',
                'billing_cycle': 'yearly',
                'price_monthly': None,
                'price_yearly': 99.99,
                'card_limit': 50,
                'social_links_limit': 15,
                'picks_limit': 200,
                'can_save_drafts': True,
                'can_hide_cards': True,
                'has_analytics': True,
                'has_google_analytics': True,
                'has_custom_templates': True,
                'has_auto_fetch': True,
                'has_youtube_api': True,
                'trial_days': 7,
                'is_active': True,
                'is_popular': False,
            }
        ]
        
        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'  📋 Created plan: {plan.name}')

    def create_card_templates(self):
        """Create card templates"""
        templates = [
            {
                'name': 'Minimal',
                'slug': 'minimal',
                'description': 'Clean and minimal design with subtle shadows',
                'font_family': 'Inter',
                'font_weights': ['300', '400', '500', '600', '700'],
                'color_scheme': {
                    'primary': '#ffffff',
                    'secondary': '#f8f9fa',
                    'accent': '#6c757d',
                    'text': '#212529'
                },
                'is_active': True,
                'is_premium': False,
                'sort_order': 1,
            },
            {
                'name': 'Modern',
                'slug': 'modern',
                'description': 'Modern design with bold colors and gradients',
                'font_family': 'Poppins',
                'font_weights': ['300', '400', '500', '600', '700', '800'],
                'color_scheme': {
                    'primary': '#8b5cf6',
                    'secondary': '#ec4899',
                    'accent': '#f59e0b',
                    'text': '#ffffff'
                },
                'is_active': True,
                'is_premium': False,
                'sort_order': 2,
            },
            {
                'name': 'Creative',
                'slug': 'creative',
                'description': 'Creative and artistic design with unique layouts',
                'font_family': 'Playfair Display',
                'font_weights': ['400', '500', '600', '700', '800', '900'],
                'color_scheme': {
                    'primary': '#f59e0b',
                    'secondary': '#f97316',
                    'accent': '#eab308',
                    'text': '#ffffff'
                },
                'is_active': True,
                'is_premium': True,
                'sort_order': 3,
            },
            {
                'name': 'Professional',
                'slug': 'professional',
                'description': 'Professional business design',
                'font_family': 'Roboto',
                'font_weights': ['300', '400', '500', '700'],
                'color_scheme': {
                    'primary': '#1f2937',
                    'secondary': '#374151',
                    'accent': '#3b82f6',
                    'text': '#ffffff'
                },
                'is_active': True,
                'is_premium': False,
                'sort_order': 4,
            },
            {
                'name': 'Colorful',
                'slug': 'colorful',
                'description': 'Bright and colorful design',
                'font_family': 'Nunito',
                'font_weights': ['300', '400', '500', '600', '700', '800'],
                'color_scheme': {
                    'primary': '#10b981',
                    'secondary': '#3b82f6',
                    'accent': '#f59e0b',
                    'text': '#ffffff'
                },
                'is_active': True,
                'is_premium': False,
                'sort_order': 5,
            }
        ]
        
        for template_data in templates:
            template, created = CardTemplate.objects.get_or_create(
                slug=template_data['slug'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'  🎨 Created template: {template.name}')

    def create_user(self, index):
        """Create a user"""
        usernames = [
            'alex_creator', 'sarah_designer', 'mike_developer', 'lisa_writer',
            'tom_photographer', 'emma_artist', 'jake_musician', 'anna_blogger',
            'david_entrepreneur', 'sophie_influencer', 'ryan_creator', 'zoe_designer',
            'max_developer', 'luna_writer', 'leo_photographer', 'maya_artist',
            'kai_musician', 'nova_blogger', 'zen_entrepreneur', 'star_influencer'
        ]
        
        names = [
            'Alex Johnson', 'Sarah Chen', 'Mike Rodriguez', 'Lisa Thompson',
            'Tom Wilson', 'Emma Davis', 'Jake Brown', 'Anna Garcia',
            'David Lee', 'Sophie Martinez', 'Ryan Taylor', 'Zoe Anderson',
            'Max White', 'Luna Jackson', 'Leo Harris', 'Maya Clark',
            'Kai Lewis', 'Nova Walker', 'Zen Hall', 'Star Young'
        ]
        
        username = usernames[index % len(usernames)]
        name = names[index % len(names)]
        first_name, last_name = name.split(' ', 1)
        
        # Create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
                'email_verified': True,
                'subscription_tier': random.choice(['free', 'pro', 'pro_trial']),
                'bio': f'Hi! I\'m {first_name}, a passionate creator sharing my journey.',
            }
        )
        
        if created:
            self.stdout.write(f'  👤 Created user: @{username}')
        
        return user

    def create_user_profile(self, user):
        """Create user profile with social links"""
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'website': f'https://{user.username}.com' if random.choice([True, False]) else '',
                'twitter': f'https://twitter.com/{user.username}' if random.choice([True, False]) else '',
                'instagram': f'https://instagram.com/{user.username}' if random.choice([True, False]) else '',
                'linkedin': f'https://linkedin.com/in/{user.username}' if random.choice([True, False]) else '',
                'youtube': f'https://youtube.com/@{user.username}' if random.choice([True, False]) else '',
                'tiktok': f'https://tiktok.com/@{user.username}' if random.choice([True, False]) else '',
                'github': f'https://github.com/{user.username}' if random.choice([True, False]) else '',
            }
        )
        return profile

    def create_user_cards(self, user, num_cards):
        """Create cards for a user"""
        card_types = ['link', 'about', 'recommendation', 'splash', 'youtube']
        templates = list(CardTemplate.objects.filter(is_active=True))
        
        for i in range(num_cards):
            card_type = random.choice(card_types)
            template = random.choice(templates)
            
            card = Card.objects.create(
                user=user,
                title=f"{user.first_name}'s {card_type.title()} Card {i+1}",
                slug=f"{card_type}-{i+1}-{user.username}",
                card_type=card_type,
                template=template,
                is_published=random.choice([True, True, True, False]),  # 75% published
                is_draft=random.choice([False, False, True]),  # 33% draft
                is_hidden=random.choice([False, False, False, True]),  # 25% hidden
                sort_order=i,
            )
            
            # Create content based on card type
            if card_type == 'link':
                self.create_link_content(card)
            elif card_type == 'about':
                self.create_about_content(card)
            elif card_type == 'recommendation':
                self.create_recommendation_content(card)
            elif card_type == 'splash':
                self.create_splash_content(card)
            elif card_type == 'youtube':
                self.create_youtube_content(card)

    def create_link_content(self, card):
        """Create link content for a card"""
        links_data = [
            {'title': 'My Website', 'url': 'https://example.com', 'link_text': 'Visit Website', 'description': 'Check out my main website'},
            {'title': 'Portfolio', 'url': 'https://portfolio.example.com', 'link_text': 'View Portfolio', 'description': 'View my latest work'},
            {'title': 'Contact Me', 'url': 'mailto:hello@example.com', 'link_text': 'Email Me', 'description': 'Get in touch with me', 'is_email': True},
            {'title': 'Call Me', 'url': 'tel:+1234567890', 'link_text': 'Call Now', 'description': 'Give me a call', 'is_phone': True},
            {'title': 'Blog', 'url': 'https://blog.example.com', 'link_text': 'Read Blog', 'description': 'Read my latest thoughts'},
        ]
        
        # Create multiple LinkContent objects for multiple links
        selected_links = random.sample(links_data, random.randint(2, 4))
        
        for i, link_data in enumerate(selected_links):
            LinkContent.objects.create(
                card=card,
                title=link_data['title'],
                description=link_data['description'],
                url=link_data['url'],
                link_text=link_data['link_text'],
                is_email=link_data.get('is_email', False),
                is_phone=link_data.get('is_phone', False),
                sort_order=i,
            )

    def create_about_content(self, card):
        """Create about content for a card"""
        about_texts = [
            "I'm a passionate creator who loves sharing knowledge and inspiring others.",
            "Welcome to my world! I create content that matters and makes a difference.",
            "Hi there! I'm on a mission to help people achieve their dreams through creativity.",
            "I believe in the power of storytelling and connecting with amazing people like you.",
            "My journey is about growth, learning, and sharing experiences with the community.",
        ]
        
        AboutContent.objects.create(
            card=card,
            title=f"About {card.user.first_name}",
            subtitle="Creator & Storyteller",
            description=random.choice(about_texts),
            heading=f"About {card.user.first_name}",
            subheading="Creator & Storyteller",
            short_description=random.choice(about_texts),
            link_text="Learn More",
            link_url="https://example.com/about",
        )

    def create_recommendation_content(self, card):
        """Create recommendation content for a card"""
        content = RecommendationContent.objects.create(
            card=card,
            title=f"{card.user.first_name}'s Top Picks",
            subtitle="My Favorite Things",
            subscription_text="Get notified about new recommendations!",
        )
        
        # Create picks
        picks_data = [
            {'title': 'Amazing Tool', 'description': 'This tool changed my workflow completely', 'link_text': 'Check it out', 'link_url': 'https://example.com/tool1'},
            {'title': 'Great Book', 'description': 'Must-read for anyone in this field', 'link_text': 'Read more', 'link_url': 'https://example.com/book1'},
            {'title': 'Cool App', 'description': 'My go-to app for productivity', 'link_text': 'Download', 'link_url': 'https://example.com/app1'},
            {'title': 'Awesome Course', 'description': 'Learn from the best in the industry', 'link_text': 'Enroll now', 'link_url': 'https://example.com/course1'},
        ]
        
        for i, pick_data in enumerate(random.sample(picks_data, random.randint(2, 4))):
            RecommendationPick.objects.create(
                recommendation=content,
                order_number=i + 1,
                **pick_data
            )

    def create_splash_content(self, card):
        """Create splash content for a card"""
        SplashContent.objects.create(
            card=card,
            title=f"Welcome to {card.user.first_name}'s World!",
            subtitle="Let's create something amazing together",
            description="Join me on this amazing journey!",
            heading=f"Welcome to {card.user.first_name}'s World!",
            subheading="Let's create something amazing together",
            link_text="Get Started",
            link_url="https://example.com/start",
        )

    def create_youtube_content(self, card):
        """Create YouTube content for a card"""
        content = YouTubeContent.objects.create(
            card=card,
            title=f"{card.user.first_name}'s Channel",
            subtitle="Subscribe for amazing content!",
            description="I create videos about creativity, productivity, and life lessons.",
            channel_url="https://youtube.com/@example",
            button_label="Subscribe",
        )
        
        # Create YouTube videos
        videos_data = [
            {'title': 'How to Get Started', 'video_url': 'https://youtube.com/watch?v=example1'},
            {'title': 'Advanced Tips', 'video_url': 'https://youtube.com/watch?v=example2'},
            {'title': 'Behind the Scenes', 'video_url': 'https://youtube.com/watch?v=example3'},
            {'title': 'Q&A Session', 'video_url': 'https://youtube.com/watch?v=example4'},
        ]
        
        for i, video_data in enumerate(random.sample(videos_data, random.randint(2, 4))):
            YouTubeVideo.objects.create(
                youtube_content=content,
                sort_order=i,
                **video_data
            )
