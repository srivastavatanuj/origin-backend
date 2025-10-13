from django.contrib import admin
from django import forms
from products.models import (
    Product,
    Category,
    Brand,
    ProductImage,
    ProductCatalog,
)


from django import forms
from .models import ProductCatalog


class ProductCatalogForm(forms.ModelForm):
    class Meta:
        model = ProductCatalog
        fields = "__all__"


class ProductCatalogAdmin(admin.ModelAdmin):
    form = ProductCatalogForm
    list_display = ("catalog__user__full_name", "product", "price")
    search_fields = ("catalog__name", "product__name")
    list_filter = ("catalog", "product")

    class Media:
        js = ("admin/js/filter_variants.js",)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country_of_origin")
    search_fields = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "brand", "get_categories", "status")
    search_fields = (
        "name",
        "sku",
    )


# class ProductVariantAdmin(admin.ModelAdmin):
#     list_display = ("product__sku", "product__name", "weight_with_unit")
#     search_fields = (
#         "product__name",
#         "product__sku",
#     )
#     ordering = ("product",)

#     def weight_with_unit(self, obj):
#         return f"{obj.weight} {obj.weight_unit}"


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product__sku", "product__name", "alt_text")
    search_fields = (
        "product__sku",
        "product__name",
    )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(ProductCatalog, ProductCatalogAdmin)

admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
