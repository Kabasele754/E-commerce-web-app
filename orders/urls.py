from django.urls import path
from .views import CheckoutView, OrderConfirmationView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-confirmation//', OrderConfirmationView.as_view(), name='order_confirmation'),

]