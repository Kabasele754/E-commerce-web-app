from django.db import models
from seller.models import Seller
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product-images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.alt_text or 'Image for {}'.format(self.id)


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)  # Notez que vous pourriez vouloir gérer les notes de manière plus complexe
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image field for product images
    images = models.ManyToManyField('ProductImage', related_name='products')

    # Many-to-many relationship for sizes
    sizes = models.ManyToManyField(Size, related_name='products')


    def get_first_image(self):
        # Récupère la première image associée au produit
        return self.images.first()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Coupon Code')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Discount Amount')
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='Valid From')
    valid_to = models.DateTimeField(null=True, blank=True, verbose_name='Valid To')
    active = models.BooleanField(default=True, verbose_name='Active')

    def clean(self):
        # Ensure that valid_from is before valid_to
        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValidationError(_('Valid from date must be before the valid to date.'))

    def __str__(self):
        return f"{self.code} - {self.discount}%"

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.active and (not self.valid_from or self.valid_from <= now) and (not self.valid_to or self.valid_to >= now)

    def get_discount(self):
        return self.discount
