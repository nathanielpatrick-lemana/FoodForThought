from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User


class CustomerAcctForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email address')
    firstname = forms.CharField(required=True, label='First name')
    lastname = forms.CharField(required=True, label='Last name')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.save()
        return user


class AcctDetUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_addr = forms.EmailField(max_length=50)
