from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Item

# Create your views here.

def inventory(request):
    items = Item.objects.all()
    template = loader.get_template('inventory/inventory.html')
    context = {
        'items': items,
    }
    return render(request, 'inventory/inventory.html', context)
