from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment, Coupon


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'billing_cycle', 'price_monthly', 'price_yearly', 'is_active', 'is_popular')
    list_filter = ('plan_type', 'billing_cycle', 'is_active', 'is_popular')
    search_fields = ('name',)
    ordering = ('plan_type', 'billing_cycle', 'price_monthly')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'billing_cycle', 'start_date', 'end_date', 'is_active')
    list_filter = ('status', 'billing_cycle', 'plan__plan_type', 'start_date')
    search_fields = ('user__username', 'user__email', 'plan__name')
    ordering = ('-start_date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'stripe_payment_intent_id')
    ordering = ('-created_at',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'coupon_type', 'discount_value', 'is_active', 'valid_from', 'valid_until')
    list_filter = ('coupon_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'name')
    ordering = ('-created_at',)
