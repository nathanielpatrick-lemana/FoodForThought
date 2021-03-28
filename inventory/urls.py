from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    #path('doughnutChart', doughnut_sales_products, name='doughnut_sales_products'),
    #path('doughtnutJSON', doughnut_chart_JSON, name='doughnut_chart_JSON'),
]
