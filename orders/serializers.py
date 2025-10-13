from gettext import Catalog
from rest_framework import serializers
from .models import Cart, Order, OrderItem, Shipping, Payment
from products.models import ProductCatalog, ProductImage
from buyers.models import ClientAddress
from products.serializers import ProductImageSerializer


class CartListSerializer(serializers.ModelSerializer):
    # Nested serializer for the ProductVariant foreign key
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.CharField(source="product.image", read_only=True)
    weight = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ("user", "image")

    def get_weight(self, obj):
        product = obj.product
        weight = str(product.weight) + product.weight_unit
        return weight

    def get_image(self, obj):
        image = ProductImage.objects.filter(product=obj.product).first()
        # handle the case where image may be None
        if image:
            return ProductImageSerializer(
                image, context={"request": self.context["request"]}
            ).data[
                "image"
            ]  # Or .data if you want the whole image data
        return None


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ("price",)
        read_only_fields = ("user",)

    def validate(self, data):
        user = self.context["request"].user
        catalog = ProductCatalog.objects.filter(catalog__user=user)
        variantIds = catalog.values_list("product", flat=True)
        if data["product"].id in variantIds:
            data["price"] = (
                data["quantity"] * catalog.get(product=data["product"].id).price
            )
            return data
        raise serializers.ValidationError(
            "Selected variant does not belong to the selected product"
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="variant.product.name", read_only=True)
    product_image = serializers.CharField(
        source="variant.product.image", read_only=True
    )
    weight = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_weight(self, obj):
        product_variant = obj.variant
        weight = str(product_variant.weight) + product_variant.weight_unit
        return weight

    def get_image(self, obj):
        # import pdb
        # pdb.set_trace()
        image = ProductImage.objects.filter(product=obj.variant.product)[0]
        return ProductImageSerializer(
            image, context={"request": self.context["request"]}
        ).data["image"]

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    name_field = serializers.SerializerMethodField()

    class Meta:
        model = Order
        exclude = ("user",)

    def get_name_field(self, obj):

        items = OrderItem.objects.filter(order=obj).values_list(
            "variant__product__name", flat=True
        )
        item_names = list(items)

        if len(item_names) > 2:
            truncated_names = item_names[:2]
            truncated_names.append("...")
            return ", ".join(truncated_names)
        else:
            return ", ".join(item_names)


class OrderShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = "__all__"


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    shipping_details = serializers.SerializerMethodField()
    # shipping_address = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_order_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        serializer_items = OrderItemSerializer(
            items, many=True, context=self.context
        ).data
        return serializer_items

    def get_shipping_details(self, obj):
        shipping = Shipping.objects.filter(order=obj)
        serializer_items = OrderShippingSerializer(shipping, many=True).data
        return serializer_items

    # def get_shipping_address(self, obj):
    #     shipping = Shipping.objects.filter(order=obj)
    #     serializer_items = OrderShippingSerializer(shipping, many=True).data
    #     return serializer_items

    def get_payment_details(self, obj):
        payment = Payment.objects.filter(order=obj)
        serializer_items = OrderPaymentSerializer(
            payment, many=True, context={"request": self.context.get("request")}
        ).data
        return serializer_items


class OrderPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        order = Order.objects.create(
            user=self.context["request"].user, **validated_data
        )
        return order
