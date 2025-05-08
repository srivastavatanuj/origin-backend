from django.db import models
from buyers.models import ClientCataloge
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='products/images/categories/', blank=True, null=True)

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


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, related_name='size', on_delete=models.CASCADE)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    size_unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    packer_length = models.FloatField()
    packer_width = models.FloatField()
    packer_height = models.FloatField()
    stock_inventory = models.PositiveIntegerField()
    expiry = models.DateField(blank=True, null=True)


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
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.catalog} - {self.product} - {self.price}"
