from gettext import Catalog
from rest_framework import serializers
from .models import Cart, Order, OrderItem, Shipping, Payment
from products.models import ProductCatalog, ProductImage
from products.serializers import ProductVariantSerializer, ProductImageSerializer


class CartListSerializer(serializers.ModelSerializer):
    # Nested serializer for the ProductVariant foreign key
    product_name = serializers.CharField(
        source='productVariant.product.name', read_only=True)
    product_image = serializers.CharField(
        source='productVariant.product.image', read_only=True)
    variant_size = serializers.CharField(
        source='productVariant.size', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('user',)

    def get_image(self, obj):
        # import pdb
        # pdb.set_trace()
        image = ProductImage.objects.filter(
            product=obj.productVariant.product)[0]
        return ProductImageSerializer(image,  context={
            'request': self.context['request']}).data['image']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ('price',)
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        catalog = ProductCatalog.objects.filter(
            catalog__user=user)
        variantIds = catalog.values_list('product_variant', flat=True)
        if data['productVariant'].id in variantIds:
            data['price'] = data['quantity'] * \
                catalog.get(product_variant=data['productVariant'].id).price
            return data
        raise serializers.ValidationError(
            'Selected variant does not belong to the selected product')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        exclude = ('user',)


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ('user',)


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    # shipping_details = serializers.SerializerMethodField()
    # paymant_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        serializer_items = OrderItemSerializer(items, many=True).data
        return serializer_items

    # def get_shipping_details(self, obj):
    #     shipping = Shipping.objects.filter(order=obj)
    #     serializer_items = OrderShippingSerializer(shipping, many=True).data
    #     return serializer_items

    # def get_paymant_details(self, obj):
    #     payment = OrderItem.objects.filter(order=obj)
    #     serializer_items = OrderItemSerializer(items, many=True).data
    #     return serializer_items


class OrderPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        order = Order.objects.create(
            user=self.context['request'].user, **validated_data)
        return order
