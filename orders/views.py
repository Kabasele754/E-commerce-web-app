from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Order, OrderItem, Payment, Customer, Product
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        try:
            customer = request.user
        except Customer.DoesNotExist:
            # Handle the case where the user doesn't have an associated customer
            return redirect('create_customer_profile')

        # Assuming you have a cart system, you'd get the cart items here
        cart_items = request.user.cart.items.all()  # This is just an example, adjust as per your cart implementation

        context = {
            'customer': customer,
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        data = request.POST
        customer = request.user

        # Create Order
        order = Order.objects.create(
            customer=customer,
            status='pending',
            total_amount=0  # We'll calculate this as we add items
        )

        # Add OrderItems
        cart_items = request.user.cart.items.all()  # Again, adjust as per your cart implementation
        total_amount = 0
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )
            total_amount += cart_item.quantity * cart_item.product.price

        # Update Order total
        order.total_amount = total_amount
        order.save()

        # Create Payment
        payment_method = data.get('paymentMethod')
        Payment.objects.create(
            order=order,
            amount=total_amount,
            method=payment_method
        )

        # Clear the cart
        request.user.cart.items.all().delete()

        # You might want to send an email confirmation here

        return JsonResponse({
            'success': True,
            'orderId': order.id,
            'message': 'Order placed successfully'
        })


# You'll also need a view for the order confirmation page
class OrderConfirmationView(LoginRequiredMixin, View):
    template_name = 'order_confirmation.html'

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
        except Order.DoesNotExist:
            return redirect('home')  # or wherever you want to redirect if order not found

        context = {
            'order': order,
        }
        return render(request, self.template_name, context)