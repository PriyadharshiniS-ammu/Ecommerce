from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type', 'is_verified')}),
        ('Contact & Address', {'fields': ('phone', 'address', 'city', 'state', 'postal_code', 'country')}),
        ('Shop Info (for sellers)', {'fields': ('shop_name', 'shop_description')}),
    )
    list_display = ['username', 'email', 'get_full_name', 'user_type', 'is_verified']
    list_filter = ['user_type', 'is_verified', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'seller']
    search_fields = ['name', 'description', 'seller__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category', 'seller', 'price', 'stock', 'image', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['added_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['buyer__username', 'buyer__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('buyer', 'status', 'created_at', 'updated_at')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'tax', 'shipping_cost', 'total_price')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['get_total_price']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['buyer__username', 'product__name']
    readonly_fields = ['created_at']
