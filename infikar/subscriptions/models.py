from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class SubscriptionPlan(models.Model):
    """Subscription plans for the platform"""
    
    PLAN_TYPES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
    ]
    
    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLES, null=True, blank=True)
    
    # Pricing
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Features and limits
    card_limit = models.PositiveIntegerField()
    social_links_limit = models.PositiveIntegerField()
    picks_limit = models.PositiveIntegerField()
    
    # Features
    can_save_drafts = models.BooleanField(default=False)
    can_hide_cards = models.BooleanField(default=False)
    has_analytics = models.BooleanField(default=False)
    has_google_analytics = models.BooleanField(default=False)
    has_custom_templates = models.BooleanField(default=False)
    has_auto_fetch = models.BooleanField(default=False)
    has_youtube_api = models.BooleanField(default=False)
    
    # Trial settings
    trial_days = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['plan_type', 'billing_cycle', 'price_monthly']
    
    def __str__(self):
        return f"{self.name} ({self.get_billing_cycle_display()})"
    
    def get_price(self, billing_cycle=None):
        """Get price for specific billing cycle"""
        if billing_cycle == 'yearly':
            return self.price_yearly
        return self.price_monthly
    
    def get_yearly_discount(self):
        """Calculate yearly discount percentage"""
        if self.price_monthly and self.price_yearly:
            monthly_yearly = self.price_monthly * 12
            if monthly_yearly > 0:
                return ((monthly_yearly - self.price_yearly) / monthly_yearly) * 100
        return 0


class UserSubscription(models.Model):
    """User subscription tracking"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('trial', 'Trial'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='user_subscriptions')
    
    # Subscription details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    billing_cycle = models.CharField(max_length=10, choices=SubscriptionPlan.BILLING_CYCLES)
    
    # Dates
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Payment details
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Auto-renewal
    auto_renew = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        if self.status == 'active':
            return self.end_date is None or self.end_date > timezone.now()
        elif self.status == 'trial':
            return self.trial_end_date and self.trial_end_date > timezone.now()
        return False
    
    @property
    def is_trial(self):
        """Check if user is in trial period"""
        return (self.status == 'trial' and 
                self.trial_end_date and 
                self.trial_end_date > timezone.now())
    
    @property
    def days_remaining(self):
        """Get days remaining in subscription or trial"""
        if self.is_trial and self.trial_end_date:
            return (self.trial_end_date - timezone.now()).days
        elif self.is_active and self.end_date:
            return (self.end_date - timezone.now()).days
        return 0
    
    def cancel(self):
        """Cancel the subscription"""
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.auto_renew = False
        self.save()
    
    def renew(self, new_end_date=None):
        """Renew the subscription"""
        self.status = 'active'
        if new_end_date:
            self.end_date = new_end_date
        else:
            # Add billing cycle to current end date or now
            if self.end_date and self.end_date > timezone.now():
                base_date = self.end_date
            else:
                base_date = timezone.now()
            
            if self.billing_cycle == 'monthly':
                self.end_date = base_date + timedelta(days=30)
            else:  # yearly
                self.end_date = base_date + timedelta(days=365)
        
        self.save()


class Payment(models.Model):
    """Payment tracking"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # External payment system
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True)
    
    # Billing period
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"


class Coupon(models.Model):
    """Discount coupons"""
    
    COUPON_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Discount details
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Applicable plans
    applicable_plans = models.ManyToManyField(SubscriptionPlan, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        """Check if coupon is currently valid"""
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_until and
                (self.usage_limit is None or self.used_count < self.usage_limit))
    
    def apply_discount(self, amount):
        """Apply discount to amount"""
        if self.coupon_type == 'percentage':
            discount = (amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:  # fixed
            discount = min(self.discount_value, amount)
        
        return max(0, amount - discount)
