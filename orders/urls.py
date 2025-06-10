from django.urls import path

from .views import CartView, OrderListView, OrderDetailView, OrderManageView, CreatePaymentLinkView, square_webhook


urlpatterns = [
    # cart
    path('cart/', CartView.as_view(), name='cart'),

    path('list/', OrderListView.as_view(), name='order-view'),
    path('list/<uuid:id>/', OrderDetailView.as_view(),
         name='order-detailedview'),
    path('create-payment-link/', CreatePaymentLinkView.as_view(), name='order-link'),
    path('place/<int:id>/', OrderManageView.as_view(), name='order-manage'),
    path("square/webhook/", square_webhook),


]
