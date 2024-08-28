from _decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Cart, Product

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Cart, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Coupon
from .forms import CouponForm
from django.core.paginator import Paginator

def product_list(request):
    products = Product.objects.all()  # Obtenez tous les produits
    paginator = Paginator(products, 3)  # Affiche 9 produits par page
    page_number = request.GET.get('page')  # Numéro de page de la requête
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = list(page_obj.object_list.values('id', 'name', 'price', 'image_url'))
        return JsonResponse({'products': products_data, 'has_next': page_obj.has_next()})

    return render(request, 'product/product_list.html', {'page_obj': page_obj})


@csrf_exempt
def add_to_cart_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        # Vérifiez si le produit est déjà dans le panier
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Si le produit est déjà dans le panier, mettez à jour la quantité
            cart_item.quantity += quantity
            cart_item.save()

        response_data = {
            'success': True,
            'message': f'{product.name} a été ajouté au panier.',
            'total_price': cart_item.get_total_price()
        }
        return JsonResponse(response_data)

    response_data = {
        'success': False,
        'message': 'Une erreur est survenue.'
    }
    return JsonResponse(response_data)


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'status': 'success'})


def view_cart(request):
    # Récupérer les éléments du panier pour l'utilisateur connecté
    cart_items = Cart.objects.filter(user=request.user)

    # Calculer le sous-total
    subtotal = sum(Decimal(item.get_total_price()) for item in cart_items)

    # Définir les frais d'expédition (vous pouvez adapter cette logique selon vos besoins)
    shipping = Decimal('4.99')  # Exemple: frais d'expédition fixe

    # Calculer le total du panier
    total = subtotal + shipping

    # Passer les valeurs au template
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })

def get_cart_data(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
        total_price = sum(item.get_total_price() for item in cart_items)
        cart_items_html = render_to_string('cart/cart_items.html', {'cart_items': cart_items})
    else:
        cart_count = 0
        total_price = 0
        cart_items_html = ""

    data = {
        'cart_count': cart_count,
        'total_price': total_price,
        'cart_items_html': cart_items_html
    }
    return JsonResponse(data)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})


def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, "Your cart has been cleared.")
    return redirect('cart')

def apply_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=code)
                request.session['coupon'] = {
                    'code': coupon.code,
                    'discount': coupon.discount,
                }
                messages.success(request, "Coupon applied successfully.")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code.")
    return redirect('cart')

def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')

