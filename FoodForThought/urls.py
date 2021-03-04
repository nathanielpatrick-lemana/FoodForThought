"""FoodForThought URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from inventory import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='customer/customer_home.html'), name='cust_home'),
    path('customer/menu/', views.menu, name='menu'),
    path('management/admin/', admin.site.urls),
    path('management/accounts/', include('accounts.urls')),
    path('management/inventory/', include('inventory.urls')),
    path('management/accounts/', include('django.contrib.auth.urls')),
    path('management/home/', TemplateView.as_view(template_name='management/management_home.html'), name='home'),
]
