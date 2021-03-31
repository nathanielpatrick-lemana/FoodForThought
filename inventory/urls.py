from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('doughnutChart/', views.doughnut_chart, name='doughnutChart'),
    path('averageDaily/', views.average_daily_sales, name='averageDaily'),
    path('averageWeekly', views.average_weekly_sales, name='averageWeekly')
]
