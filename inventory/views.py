from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import user_passes_test
from .models import Item
from .models import Ingredients
from .models import ItemStockLevels
from .models import CustomerOrders
from .models import Orders
import datetime
from .forms import OrderForm
from .forms import IngredientForm
import random
from django.forms import formset_factory
from django.http import JsonResponse


# Create your views here.

def employee(user):
    return user.groups.filter(name='Employee').exists()


def menu(request):
    items = Item.objects.all()
    template = loader.get_template('customer/menu.html')
    context = {
        'items': items,
    }
    return render(request, 'customer/menu.html', context)


def order(request):
    items = Item.objects.all()

    # creating a formset
    OrderFormSet = formset_factory(OrderForm, extra=10)
    formset = OrderFormSet(request.POST or None, initial=0)

    if formset.is_valid():
        new_id = random.randint(1000, 9999)
        counter = 1
        neworder = Orders(new_id, datetime.date.today())
        neworder.save()
        for form in formset:
            quantity = form.cleaned_data.get('item_quantity', 0)
            custor = CustomerOrders(counter * new_id, new_id, counter, quantity)
            custor.save()
            counter = counter + 1
        context = {
            'new_id': new_id,
        }
        return render(request, "customer/order_confirmed.html", context)

    # Add the formset to context dictionary
    context = {
        'items': items,
        'formset': formset,
    }
    return render(request, "customer/order.html", context)


@user_passes_test(employee)
def inventory(request):
    form = IngredientForm(request.POST or None)
    instocks = Ingredients.objects.all()
    ingredients = ItemStockLevels.objects.all()
    template = loader.get_template('inventory/inventory.html')
    if form.is_valid():
        newing = Ingredients(len(Ingredients.objects.filter()) + 1, form.cleaned_data.get('name'), 30, 'unit')
        newing2 = ItemStockLevels(len(ItemStockLevels.objects.filter()) + 1, len(ItemStockLevels.objects.filter()) + 1,
                                  form.cleaned_data.get('name'), form.cleaned_data.get('quantity'),
                                  datetime.date.today(), )
        newing.save()
        newing2.save()
        context = {
            'ingredients': ingredients,
            'instocks': instocks,
            'form': form,
        }
        return render(request, 'inventory/inventory.html', context)
    context = {
        'ingredients': ingredients,
        'instocks': instocks,
        'form': form,
    }
    return render(request, 'inventory/inventory.html', context)


@user_passes_test(employee)
def suppman(request):
    instocks = Ingredients.objects.all()
    ingredients = ItemStockLevels.objects.all()
    template = loader.get_template('inventory/suppman.html')
    context = {
        'ingredients': ingredients,
        'instocks': instocks,
    }
    return render(request, 'inventory/suppman.html', context)


@user_passes_test(employee)
def sales(request):
    instocks = Ingredients.objects.all()
    ingredients = ItemStockLevels.objects.all()
    template = loader.get_template('inventory/sales.html')
    context = {
        'ingredients': ingredients,
        'instocks': instocks,
    }
    return render(request, 'inventory/sales.html', context)


def PieSalesChart(request):

    template = 'templates/inventory/sales.html'

    return render(request, template)



