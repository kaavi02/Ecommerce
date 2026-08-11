from django.contrib import admin
from .models import Product, CartItem, WishlistItem, Order, UserProfile

admin.site.site_header = "KavyNest Administration"
admin.site.site_title = "KavyNest Portal"
admin.site.index_title = "Welcome to KavyNest Management"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_mode', 'payment_status', 'created_at')
    list_filter = ('payment_mode', 'payment_status')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'security_question')

admin.site.register(CartItem)
admin.site.register(WishlistItem)