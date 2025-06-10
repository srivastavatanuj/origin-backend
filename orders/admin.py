from django.contrib import admin
from .models import Cart, Order, OrderItem, Payment, Shipping
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'productVariant', 'quantity', 'price')
    search_fields = ('user__email', 'productVariant__product__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_amount', 'status')
    search_fields = ('id', 'user__email', 'status')
    list_filter = ('status', 'created_at')
    readonly_fields = ('id', 'created_at')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'variant', 'quantity', 'price')
    search_fields = ('order__id', 'variant__product__name')
    list_filter = ('order__id',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'order_id',
                    'amount', 'payment_status', 'created_at',)
    search_fields = ('order_id', 'payment_id', 'payment_status',)
    list_filter = ('payment_method', 'payment_status',)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order', 'address', 'deliveryService',
                    'trakingId', 'status')
    search_fields = ('order__id', 'trakingId', 'status')
    list_filter = ('status', 'deliveryService')
