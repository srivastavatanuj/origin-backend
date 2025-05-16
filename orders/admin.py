from django.contrib import admin
from .models import Cart, Order, OrderItem, Payment, Shipping
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipping)
