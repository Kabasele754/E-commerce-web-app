# admin.py
from django.contrib import admin
from .models import Product, ProductImage, Size, Category


class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'rating')
    inlines = [ProductImageInline]

class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(Category)
