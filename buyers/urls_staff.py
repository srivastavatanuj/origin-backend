from django.urls import path
from .views_staff import *

urlpatterns = [
    path('add/', StaffCreateView.as_view(), name='staff-create'),
    path('list/', StaffListView.as_view(), name='staff-list'),
    path('list/<int:pk>/', StaffManageView.as_view(), name='staff-manage'),


]
