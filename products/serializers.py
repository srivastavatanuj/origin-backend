from rest_framework import serializers
from .models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductCatalog,
)

# BRAND


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


# CATEGORY


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# PRODUCT


class ProductSerializer(serializers.ModelSerializer):
    # or use PrimaryKeyRelatedField
    category = CategorySerializer(many=True, read_only=True)
    items_per_page = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_items_per_page(self, obj):
        return 8

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(
            images, many=True, context={"request": self.context["request"]}
        ).data


class ViewProductSerializer(serializers.ModelSerializer):
    # or use PrimaryKeyRelatedField
    category = CategorySerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(
            images, many=True, context={"request": self.context["request"]}
        ).data


# VARIANT


# class ProductVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariant
#         fields = '__all__'

# IMAGE


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


# CATALOGE


class ProductCatalogeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCatalog
        fields = "__all__"

    def validate(self, data):
        product = data.get("product")
        variant = data.get("product_variant")

        if product and variant and variant.product != product:
            raise serializers.ValidationError(
                "Selected variant does not belong to the selected product."
            )
        return data


class MyCatalogeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProductCatalog
        fields = "__all__"

    def get_name(self, obj):
        return obj.product.name

    def get_images(self, obj):
        images = ProductImage.objects.filter(product=obj.product)
        return ProductImageSerializer(
            images, many=True, context={"request": self.context["request"]}
        ).data

        return serializer.data["image"]

    def get_description(self, obj):
        return obj.product.description


class MyCatalogeProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"


class MyCatalogeProductVarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
