from django.contrib import admin
from .models import Product, Cart, CartItem, Order, Contact, PasswordResetOTP
# Register your models here.

#Display product in admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')

# register cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

#Register cart items model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')

# Register Order Model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'items', 'total_price', 'created_at')  # Make these fields read-only to prevent admin errors
    filter_horizontal = ('items',)  # Optional: better UI for ManyToMany field

# Contact 
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message', 'created_at')
    

@admin.register(PasswordResetOTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'otp', 'created_at')