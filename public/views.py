from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from products.models import Product, Category


# Create your views here.

class HomePageView(TemplateView):
    template_name = "public/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les produits et les catégories depuis la base de données
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        return context

