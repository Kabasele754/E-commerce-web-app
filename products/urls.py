from django.urls import path
from . import views
from .views import add_to_cart_ajax, product_detail

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-data/', views.get_cart_data, name='header_cart_data'),
 path('add-to-cart-ajax/', add_to_cart_ajax, name='add_to_cart_ajax'),
  path('product/<int:product_id>/', product_detail, name='product_detail'),

    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

path('shop/', views.product_list, name='shop'),


]
