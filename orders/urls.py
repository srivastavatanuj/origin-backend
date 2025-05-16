from django.urls import path
from .views import *


from .views import (
    CartView,
    OrderListView, OrderDetailView, OrderPlaceView, OrderManageView, CreatePaymentLinkView
)

urlpatterns = [
    # cart
    path('cart/', CartView.as_view(), name='cart'),

    path('list/', OrderListView.as_view(), name='order-view'),
    path('list/<int:id>/', OrderDetailView.as_view(), name='order-detailedview'),
    path('create-payment-link/', CreatePaymentLinkView.as_view(), name='order-link'),
    path('place/', OrderPlaceView.as_view(), name='order-place'),
    path('place/<int:id>/', OrderManageView.as_view(), name='order-manage'),
]
