from django.urls import path
from .views import QuickBookCallback, QuickBookLogin

urlpatterns = [
    path('login/', QuickBookLogin.as_view(), name='quickbook_login'),
    path('callback/', QuickBookCallback.as_view(), name='quickbook_callback'),
    # path('log-payment/', LogPaymentToQuickBooks.as_view(), name='log_payment'),
]
