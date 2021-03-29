from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('doughnutChart/', views.doughnut_chart, name='doughnutChart'),
    #path('doughtnutJSON', doughnut_chart_JSON, name='doughnut_chart_JSON'),
]
