from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import user_passes_test
from .models import Item
from .models import Ingredients
from .models import ItemStockLevels


# Create your views here.

def employee(user):
    return user.groups.filter(name='Employee').exists()


def menu(request):
    items = Item.objects.all()
    template = loader.get_template('customer/order.html')
    context = {
        'items': items,
    }
    return render(request, 'customer/order.html', context)


@user_passes_test(employee)
def inventory(request):
    instock = Ingredients.objects.all()
    ingredients = ItemStockLevels.objects.all()
    template = loader.get_template('inventory/inventory.html')
    context = {
        'ingredients': ingredients,
        'instocks': instock,
    }
    return render(request, 'inventory/inventory.html', context)
