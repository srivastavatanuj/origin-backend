from django.contrib import admin
from products.models import Product, Category, Brand, ProductImage, ProductVariant, ProductCatalog
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductCatalog)
