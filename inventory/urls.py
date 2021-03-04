from django.urls import path

from . import views

urlpatterns = [

    path('', views.inventory, name='inventory'),
    path('menu', views.menu, name='menu')
]
