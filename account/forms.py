from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User


class CustomerAcctForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user
