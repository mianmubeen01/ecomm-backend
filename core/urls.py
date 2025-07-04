from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('api/', include(router.urls)),  # This line is important
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', current_user),
    path('rest/', include('rest_framework.urls')),
    path('api/contact/', ContactVIew.as_view(), name= 'contact'),
    path("api/stripe/", views.Stripe_Checkout, name = 'stripe_checkout'),
    path('api/forgot-password/', ForgotPasswordView.as_view()),
    path('api/verify-otp/', VerifyOTPView.as_view()),
    path('api/reset-password/', ResetPasswordView.as_view()),
    path('api/resend-otp/', ResendOTPView.as_view()),
]
