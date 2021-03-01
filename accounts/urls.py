from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('management/signup/', SignUpView.as_view(), name='signup'),
]