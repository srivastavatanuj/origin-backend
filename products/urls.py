from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin
    path("brand/list/", ListProductBrandView.as_view(), name="brand_list"),
    path("brand/list/<int:id>/", ManageProductBrandView.as_view(), name="brand_manage"),
    path("category/list/", ListProductCategoryView.as_view(), name="category_list"),
    path(
        "category/list/<int:id>/",
        ManageProductCategoryView.as_view(),
        name="category_manage",
    ),
    path("product/list/", ListProductView.as_view(), name="product_list"),
    path("product/list/<str:pk>/", ManageProductView.as_view(), name="product_manage"),
    #     path('variant/list/', ListProductVariantView.as_view(), name='variant_list'),
    #     path('variant/list/<int:id>/',
    #          ManageProductVariantView.as_view(), name='variant_manage'),
    path("image/list/", ListProductImageView.as_view(), name="image_list"),
    path("image/list/<int:id>/", ManageProductImageView.as_view(), name="image_manage"),
    path("catalog/list/", ListProductCatalogeView.as_view(), name="customcatalog_list"),
    path(
        "catalog/list/<int:id>/",
        ManageProductCatalogeView.as_view(),
        name="customcatalog_manage",
    ),
    # user
    path("allproducts/", ViewAllProductView.as_view(), name="product_list"),
    path("my-cataloge/", MyCatalogeView.as_view(), name="cataloge"),
    path(
        "my-cataloge/<str:pk>/", MyCatalogeProductView.as_view(), name="product_manage"
    ),
    # path(
    #     "my-cataloge/<str:pk>/<int:id>/",
    #     MyCatalogeProductVarientView.as_view(),
    #     name="product_manage",
    # ),
]
