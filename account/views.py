from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import User
from .forms import CustomerAcctForm


class CustomerSignup(CreateView):
    model = User
    form_class = CustomerAcctForm
    success_url = reverse_lazy('/registration/login')
    template_name = 'customer/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('cust_home')
