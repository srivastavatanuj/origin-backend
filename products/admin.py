from django.contrib import admin
from django import forms
from products.models import Product, Category, Brand, ProductImage, ProductVariant, ProductCatalog


from django import forms
from .models import ProductCatalog, ProductVariant


class ProductCatalogForm(forms.ModelForm):
    class Meta:
        model = ProductCatalog
        fields = '__all__'


class ProductCatalogAdmin(admin.ModelAdmin):
    form = ProductCatalogForm

    class Media:
        js = ('admin/js/filter_variants.js',)


admin.site.register(ProductCatalog, ProductCatalogAdmin)

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
