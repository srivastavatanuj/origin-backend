from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from yaml import serialize

from .models import Cart, Order, OrderItem, Payment, Shipping
from products.models import Product, ProductCatalog
from buyers.models import ClientAddress, ClientCataloge
from .serializers import (
    CartSerializer,
    OrderSerializer,
    OrderDetailSerializer,
    OrderPlaceSerializer,
    CartListSerializer,
)
from django.db.models import Sum
import pdb
from rest_framework.exceptions import NotFound
import uuid
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from django.db.models import Q


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartListSerializer

    def get(self, request):
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        price = Cart.objects.filter(user=user).aggregate(Sum("price"))

        serializer = self.serializer_class(
            cart, many=True, context={"request": request}
        ).data
        # product_name=
        # product_image =
        # variant_size =
        data = {"cart_items": serializer, "total_price": price}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        sku = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        # Get user's catalog
        user_catalog = ClientCataloge.objects.get(user=user)
        if user_catalog.default_cataloge:
            catalog_products = ProductCatalog.objects.filter(catalog_id=1)
        else:
            catalog_products = ProductCatalog.objects.filter(catalog__user=user)

        # Get product by SKU
        product = get_object_or_404(Product, sku=sku)

        # Try to find in catalog
        catalog_entry = catalog_products.filter(product__sku=sku).first()

        # Determine correct price
        if user_catalog.pricing_enabled:
            product_price = catalog_entry.price
        else:
            product_price = getattr(product, "price", 0)

        # Check if product already in cart
        try:
            cart_item = Cart.objects.get(user=user, product=product)
            cart_item.quantity += 1
            cart_item.price = cart_item.quantity * product_price
            print(cart_item)
        except Cart.DoesNotExist:
            cart_item = Cart.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                price=quantity * product_price,
            )

        cart_item.save()
        return Response(
            {"details": "Item added successfully"}, status=status.HTTP_201_CREATED
        )

    def put(self, request):
        user = self.request.user
        currectVar = request.data["product"]
        cart = get_object_or_404(Cart, product_id=currectVar)
        item_price = cart.price / cart.quantity
        cart.quantity = request.data["quantity"]
        cart.price = cart.quantity * item_price
        cart.save()
        return Response(
            {"details": "Item updated Successfully"}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        user = self.request.user
        currectVar = request.data["product"]
        cart = get_object_or_404(Cart, product_id=currectVar)
        cart.delete()
        return Response(
            {"details": "Item deleted Successfully"}, status=status.HTTP_200_OK
        )


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(views.APIView):
    def get(self, request, id):

        orders = Order.objects.filter(id=id)
        serializer = OrderDetailSerializer(
            orders, many=True, context={"request": request}
        )
        return Response(serializer.data)


class CreatePaymentLinkView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderPlaceSerializer

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)

        if not cart.exists():
            return Response(
                {"details": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = cart.aggregate(total=Sum("price"))["total"] or 0
        order = Order.objects.create(user=user, total_amount=total_price)

        try:
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price,
                )
        except Exception as e:
            order.delete()
            return Response(
                {"details": "Order creation failed", "error": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        # 🎯 Create Square Payment Link
        url = "https://connect.squareupsandbox.com/v2/online-checkout/payment-links"
        headers = {
            "Authorization": f"Bearer {os.getenv('SQUAREUP_TEST_TOKEN')}",
            "Content-Type": "application/json",
        }
        print(f"Bearer {os.getenv('SQUAREUP_TEST_TOKEN')}", url)

        payload = {
            "idempotency_key": str(uuid.uuid4()),
            "order": {
                "location_id": os.getenv(
                    "LOCATION_ID"
                ),  # replace with actual location ID
                "line_items": [
                    {
                        "name": (
                            str(item.product)
                            if hasattr(item, "product")
                            else str(item.product.name)
                        ),
                        "quantity": str(item.quantity),
                        "base_price_money": {
                            "amount": int(item.price / item.quantity * 100),
                            "currency": "CAD",
                        },
                    }
                    for item in cart
                ],
            },
            "checkout_options": {
                "redirect_url": os.getenv("PAYMENT_GATEWAY_REDIRECT_URL")
                + str(order.id),
            },
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if response.status_code in [200, 201]:
            payment_link = data.get("payment_link")
            if not payment_link:
                return Response(
                    {"details": "Missing payment link data", "response": data},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            payment_url = payment_link.get("url")
            payment_id = payment_link.get("id")
            created_at = payment_link.get("created_at")
            amount = total_price  # use your local calculated total

            Payment.objects.create(
                payment_id=payment_id,
                amount=amount,
                payment_method="SquareUp",
                created_at=created_at,
                order_id=order,
                payment_status="PENDING",
            )

            # Optional: Clear cart after creating order
            cart.delete()

            return Response(
                {
                    "details": "Order created successfully",
                    "payment_url": payment_url,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            order.delete()  # cleanup failed order
            return Response(
                {
                    "details": "Order created but failed to generate payment link",
                    "square_response": data,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@csrf_exempt
def square_webhook(request):
    payload = json.loads(request.body)
    event_type = payload.get("type")

    if event_type == "payment.updated":
        payment = payload["data"]["object"]["payment"]
        status_str = payment.get("status")
        payment_id = payment.get("id")

        if status_str == "COMPLETED":
            try:
                pay = Payment.objects.get(payment_id=payment_id)
                pay.status = "COMPLETED"
                pay.save()

                order = pay.order
                order.status = "PAID"
                order.save()

            except Payment.DoesNotExist:
                pass

    return Response({"status": "ok"}, status=status.HTTP_200_OK)


class OrderManageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
