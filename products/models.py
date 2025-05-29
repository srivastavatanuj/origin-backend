from django.db import models
from buyers.models import ClientCataloge
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to='products/images/brands/', blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ])
    barcode = models.CharField(max_length=100, blank=True)
    supplier_note = models.TextField(blank=True)

    category = models.ManyToManyField(Category, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_categories(self):
        return ", ".join([category.name for category in self.category.all()])


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_variant', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    weight_unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    packer_length = models.FloatField(blank=True, null=True)
    packer_width = models.FloatField(blank=True, null=True)
    packer_height = models.FloatField(blank=True, null=True)
    stock_inventory = models.PositiveIntegerField()
    expiry = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.product}-{self.weight}{self.weight_unit}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/products/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductCatalog(models.Model):
    catalog = models.ForeignKey(
        ClientCataloge, on_delete=models.SET_NULL, null=True, related_name='custom_catalog'
    )
    product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.name} [{self.product.id}]"
