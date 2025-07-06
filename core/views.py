from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
# Stripe Payment Logic
import stripe
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# OTP 
import random
from .models import PasswordResetOTP  
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.views import APIView

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]


# For Registering User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# get current user info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        'username': request.user.username,
        'is_staff': request.user.is_staff,
    })

# Cart Logic
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = item.quantity + quantity if not created else quantity
        item.save()
        return Response(CartSerializer(cart).data, status=201)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response(CartSerializer(cart).data, status=200)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not in cart'}, status=404)

    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.quantity = quantity
            item.save()
            return Response(CartSerializer(cart).data, status=200)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=404)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'}, status=200)
        
# ORder Logic
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            print(cart, "cart")
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

        items = cart.items.all()
        print(items, 'items')
        if not items:
            return Response({'error': 'Cart is empty'}, status=400)

        total = sum([item.product.price * item.quantity for item in items])

        # Get address, phone, and payment method from request
        address = request.data.get('address', 'N/A')
        phone_number = request.data.get('phone_number', 'N/A')
        payment_method = request.data.get('payment_method', 'cash')
        is_paid = request.data.get('is_paid', False)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            address=address,
            phone_number=phone_number,
            payment_method=payment_method,
            is_paid=is_paid,
            
        )

        # Link cart items to order
        order.items.set(items)
        print(order.items)
        order.save()


        # Return response with serialized data
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)

    
# Contact Logic
class ContactVIew(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
        


# Set your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def Stripe_Checkout(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": data.get("currency", "usd"),
                            "product_data": {
                                "name": data["product_name"],
                            },
                            "unit_amount": int(float(data["amount"]) * 100),
                        },
                        "quantity": data.get("quantity", 1),
                    },
                ],
                mode="payment",
                success_url=data.get("success_url", "http://localhost:3000/success"),
                cancel_url=data.get("cancel_url", "http://localhost:3000/cancel"),
            )
            return JsonResponse({"id": session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)
    
# OTP Logic
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email"}, status=404)

        otp = str(random.randint(1000, 9999))

        # Save or update OTP
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="Your OTP for password reset",
            message=f"Your One-Time Password (OTP) is: {otp}. It will expire in 2 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"message": "OTP sent to email."}, status=200)

# Verify OTP
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=400)

        try:
            user = User.objects.get(email=email)
            otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp).last()

            if not otp_record:
                return Response({"error": "Invalid OTP"}, status=400)

            if not otp_record.is_valid():  # ✅ lowercase method name
                return Response({"error": "OTP expired"}, status=400)

            return Response({"message": "OTP verified", "uid": user.id}, status=200)

        except User.DoesNotExist:
            return Response({"error": "Invalid email"}, status=400)


# Resend OTP
class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)

            # Generate and save new OTP
            otp = str(random.randint(1000, 9999))
            PasswordResetOTP.objects.update_or_create(
                user=user,
                defaults={"otp": otp, "created_at": timezone.now()}
            )

            subject = "Your OTP Code"
            message = f"Hi {user.username},\n\nYour new OTP code is: {otp}"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            return Response({"message": "OTP resent successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=404)

# Reset Password
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        password = request.data.get("password")

        if not uid or not password:
            return Response({"error": "UID and password are required"}, status=400)

        try:
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)
