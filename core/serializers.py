from rest_framework import serializers
from .models import Product, Cart, CartItem, Order, Contact
from django.contrib.auth.models import User

# ------------------------------
# Product Serializer
# ------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ------------------------------
# Registration Serializer
# ------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ------------------------------
# User Serializer (for login/info display)
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ------------------------------
# Cart Item Serializer
# ------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'line_total']

    def get_line_total(self, obj):
        return obj.quantity * obj.product.price


# ------------------------------
# Cart Serializer
# ------------------------------
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']


# ------------------------------
# Order Serializer
# ------------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'items', 'total_price',
            'address', 'phone_number', 'payment_method',
            'is_paid', 'created_at'
        ]
        read_only_fields = ['user', 'total_price',  'created_at']


# ------------------------------
# Contact Serializer
# ------------------------------
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
