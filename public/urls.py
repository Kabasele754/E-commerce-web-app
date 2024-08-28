
from django.urls import path, include

from products.views import view_cart
from public.views import HomePageView

urlpatterns = [

    path('', HomePageView.as_view(), name="home"),
    path('cart/', view_cart, name='cart')

]