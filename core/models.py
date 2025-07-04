from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import  timedelta

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=150)
    rating = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    company = models.CharField(max_length=100, null=True, blank=True)
    stars = models.FloatField(null=True, blank=True)
    reviews = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    # for Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default="N/A")
    phone_number = models.CharField(max_length=20, default="N/A")
    payment_method = models.CharField(max_length=50, default="N/A")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    
# OTP Model
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <self.created_at + timedelta(minutes=2)
    