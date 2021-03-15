from django.urls import path

from . import views

urlpatterns = [

    path('', views.inventory, name='inventory'),
    path('pie-chart-sales/', views.PieSalesChart, name='sales-pie-chart'),
]
