from django.urls import path
from .views import *


urlpatterns = [
    path('brand/list/', ListProductBrandView.as_view(), name='brand_list'),
    path('brand/list/<int:id>/',
         ManageProductBrandView.as_view(), name='brand_manage'),

    path('category/list/', ListProductCategoryView.as_view(), name='category_list'),
    path('category/list/<int:id>/',
         ManageProductCategoryView.as_view(), name='category_manage'),

    path('list/', ListProductView.as_view(), name='product_list'),
    path('list/<str:pk>/', ManageProductView.as_view(), name='product_manage'),

    path('variant/list/', ListProductVariantView.as_view(), name='variant_list'),
    path('variant/list/<int:id>/',
         ManageProductVariantView.as_view(), name='variant_manage'),

    path('image/list/', ListProductImageView.as_view(), name='image_list'),
    path('image/list/<int:id>/',
         ManageProductImageView.as_view(), name='image_manage'),

    path('catalog/list/', ListProductCatalogeView.as_view(),
         name='customcatalog_list'),
    path('catalog/list/<int:id>/', ManageProductCatalogeView.as_view(),
         name='customcatalog_manage'),
]
