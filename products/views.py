from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Brand, Category, Product, ProductVariant, ProductImage, ProductCatalog
from .serializers import (
    BrandSerializer, CategorySerializer, ProductSerializer,
    ProductVariantSerializer, ProductImageSerializer, ProductCatalogeSerializer
)
from buyers.permissions import IsAdminOrManager
from faker import Faker
import random

from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import random
import io
from PIL import Image

# BRAND


class ListProductBrandView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrManager]


class ManageProductBrandView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManager]

# CATEGORY


class ListProductCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrManager]


class ManageProductCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManager]

# PRODUCT


class ListProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]


class ManageProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]

# VARIANT


class ListProductVariantView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminOrManager]


class ManageProductVariantView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManager]

# IMAGE


class ListProductImageView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrManager]


class ManageProductImageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManager]

# CATALOGE


class ListProductCatalogeView(generics.ListCreateAPIView):
    queryset = ProductCatalog.objects.all()
    serializer_class = ProductCatalogeSerializer
    permission_classes = [IsAdminOrManager]


class ManageProductCatalogeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCatalog.objects.all()
    serializer_class = ProductCatalogeSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManager]


def fake_brand():
    fake = Faker()
    for _ in range(5):
        Brand.objects.create(
            name=fake.name(), logo=get_random_image(), country_of_origin=fake.country())


def fake_category():
    fake = Faker()
    for _ in range(5):
        Category.objects.create(
            name=fake.name(), description=fake.text(), logo=get_random_image())


def get_random_image():
    fake = Faker()
    # generate a random image in memory
    image = Image.new('RGB', (100, 100), color=fake.color())
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f"{fake.word()}.png")


def fake_product():
    fake = Faker()
    brands = Brand.objects.all()
    categories = Category.objects.all()

    for _ in range(20):  # number of products
        brand = random.choice(brands)
        product = Product.objects.create(
            sku=fake.unique.bothify(text='???-#####'),
            name=fake.word().capitalize(),
            description=fake.text(),
            status=random.choice(['active', 'inactive', 'discontinued']),
            barcode=fake.ean13(),
            supplier_note=fake.text(),
            brand=brand
        )
        product.category.set(random.sample(
            list(categories), k=random.randint(1, 3)))

        # Images
        for _ in range(random.randint(1, 3)):
            ProductImage.objects.create(
                product=product,
                image=get_random_image(),
                alt_text=fake.sentence()
            )

        # Variants
        for _ in range(random.randint(1, 4)):
            ProductVariant.objects.create(
                product=product,
                size=round(random.uniform(100, 500), 2),
                size_unit=random.choice(['g', 'kg', 'ml', 'L']),
                price=round(random.uniform(10, 100), 2),
                packer_length=random.uniform(5, 20),
                packer_width=random.uniform(5, 20),
                packer_height=random.uniform(5, 20),
                stock_inventory=random.randint(1, 100),
                expiry=fake.future_date()
            )
