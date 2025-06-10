from gettext import Catalog
from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .models import Brand, Category, Product, ProductVariant, ProductImage, ProductCatalog
from .serializers import (
    BrandSerializer, CategorySerializer, ProductSerializer,
    ProductVariantSerializer, ProductImageSerializer, ProductCatalogeSerializer, ViewProductSerializer, MyCatalogeProductVarientSerializer, MyCatalogeProductSerializer, MyCatalogeSerializer
)
from buyers.permissions import IsAdminOrManager
from faker import Faker
import random
from django.shortcuts import get_object_or_404

from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
import random
import io
from PIL import Image
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# paginatoion


class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

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
    pagination_class = CustomPagination


class ManageProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]


class ViewAllProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ViewProductSerializer
    permission_classes = [AllowAny]


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


class MyCatalogeView(generics.ListAPIView):
    serializer_class = MyCatalogeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductCatalog.objects.filter(catalog__user=user)


class MyCatalogeProductView(views.APIView):
    serializer_class = ViewProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        catalog_entries = ProductCatalog.objects.filter(
            catalog__user=user, product__pk=pk)

        product = get_object_or_404(Product, pk=pk)

        variant_ids = catalog_entries.values_list('product_variant', flat=True)
        product_ids = catalog_entries.values_list('product', flat=True)
        variants = ProductVariant.objects.filter(id__in=variant_ids)

        product_data = ProductSerializer(
            product, context={'request': request}).data
        variant_data = ProductVariantSerializer(variants, many=True).data

        catalog_entries_map = {
            entry.product_variant.id: entry.price for entry in catalog_entries}

        if catalog_entries[0].catalog.pricing_enabled:
            for variant in variant_data:
                var_id = variant['id']
                if var_id in catalog_entries_map:
                    variant['price'] = str(catalog_entries_map[var_id])

        if pk in product_ids:
            return Response({
                "product": product_data,
                "variants": variant_data
            })
        else:
            return Response(
                {"error": "Product not found in the user's catalog."},
                status=status.HTTP_404_NOT_FOUND
            )


class MyCatalogeProductVarientView(generics.RetrieveAPIView):
    serializer_class = MyCatalogeProductVarientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()


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
