from django.shortcuts import render
from .models import Cart


def header_cart_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
        total_price = sum(item.get_total_price() for item in cart_items)
    else:
        cart_items = []
        cart_count = 0
        total_price = 0

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'total_price': total_price,
    }
