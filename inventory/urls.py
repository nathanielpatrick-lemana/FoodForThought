from django.urls import path

from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('doughnutChart/', views.doughnut_chart, name='doughnutChart'),
    path('averageDaily/', views.average_daily_sales, name='averageDaily'),
    path('averageWeekly', views.average_weekly_sales, name='averageWeekly'),
    path('stockconsumption/', views.stock_consumption, name='stockConsumption'),
    path('dailyrev/', views.daily_revenue, name='dailyRev'),
    path('weeklyrev/', views.weekly_revenue, name='weeklyRev')
]
