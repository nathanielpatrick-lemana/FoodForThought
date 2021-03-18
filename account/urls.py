from django.urls import path

from .views import CustomerSignup

urlpatterns = [
    path('customer/signup/', CustomerSignup.as_view(), name='custsignup'),
]