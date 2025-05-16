from django.urls import path
from .views import ContactUsListView, ContactUsCreateView, ContactUsRetrieveUpdateDestroyView

urlpatterns = [
    path('contact-us/list/', ContactUsListView.as_view(),
         name='contactus-list-create'),
    path('contact-us/', ContactUsCreateView.as_view(),
         name='contactus-list-create'),
    path('contact-us/<int:pk>/', ContactUsRetrieveUpdateDestroyView.as_view(),
         name='contactus-retrieve-update-destroy'),
]
