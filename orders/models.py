from django.db import models
from buyers.models import User, ClientAddress
from products.models import Product
import uuid

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.variant} in Order #{self.order.id}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refund", "Refunded"),
    )
    payment_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=50)  # e.g., 'Razorpay', 'Stripe'
    payment_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Shipping(models.Model):
    STATUS_CHOICE = (
        ("notshipped", "Not Shipped Yet"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("delayed", "Delayed"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="shipping")
    address = models.ForeignKey(
        ClientAddress, on_delete=models.DO_NOTHING, related_name="shippingAddress"
    )
    deliveryService = models.CharField(max_length=30, blank=True, null=True)
    trakingId = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        choices=STATUS_CHOICE, default="notshipped", max_length=50
    )
