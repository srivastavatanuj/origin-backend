from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views_auth import *

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('reset/<str:hash>/', ResetView.as_view(), name='reset'),
    path('change-password/', ChangePasswordView.as_view(), name='reset'),
]
