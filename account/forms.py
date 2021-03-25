from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User


class CustomerAcctForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email address')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data["email"]
        user.save()
        return user
