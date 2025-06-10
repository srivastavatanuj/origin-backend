from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import generics
from .models import ContactUs
from .serializers import ContactUsSerializer
from rest_framework.permissions import AllowAny
from buyers.permissions import IsAdminOrManager


class ContactUsCreateView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


class ContactUsListView(generics.ListAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrManager]


class ContactUsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrManager]
