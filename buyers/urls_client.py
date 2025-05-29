from django.urls import path
from .views_client import *

urlpatterns = [
    # admin only
    path('list/', ListClientView.as_view(), name='staff-profile'),
    path('list/<int:pk>/', ManageClientView.as_view(), name='staff-profile'),

    path('business/listall/', ListClientBusinessView.as_view(),
         name='client-businesslist'),
    path('business/listall/<int:pk>/',
         ManageClientBusinessView.as_view(), name='client-business-edit'),

    path('cataloge/listall/', ListClientCatalogeView.as_view(),
         name='client-catalogelist'),
    path('cataloge/listall/<int:pk>/',
         ManageClientCatalogeView.as_view(), name='client-cataloge-edit'),

    path('address/listall/', ListClientAddressView.as_view(),
         name='client-addresslist'),
    path('address/listall/<int:pk>/',
         ManageClientAddressView.as_view(), name='client-address-edit'),

    # user
    path('business/', ClientBusinessView.as_view(), name='client-business'),
    path('cataloge/', ClientCatalogeView.as_view(), name='client-cataloge'),
    path('address/', ClientAddressView.as_view(), name='client-address'),
    path('user/', ClientUserView.as_view(), name='client-user'),
     path('profile/', ClientProfileView.as_view(), name='client-profile'),
]
