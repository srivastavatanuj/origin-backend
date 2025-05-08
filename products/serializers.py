from rest_framework import serializers
from .models import (
    Brand, Category, Product, ProductVariant,
    ProductImage, ProductCatalog
)

# BRAND


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

# CATEGORY


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# PRODUCT


class ProductSerializer(serializers.ModelSerializer):
    # or use PrimaryKeyRelatedField
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

# VARIANT


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

# IMAGE


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

# CATALOGE


class ProductCatalogeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCatalog
        fields = '__all__'
