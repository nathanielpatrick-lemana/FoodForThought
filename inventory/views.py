from django.shortcuts import render
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from .models import Item
from .models import Ingredients
from .models import ItemStockLevels
from .models import CustomerOrders
from .models import Orders
import datetime
from .forms import OrderForm
from .forms import IngredientForm
from .forms import RestockForm
from .forms import PushOrder
import random
from django.forms import formset_factory
from django.core.mail import send_mail
from django.http import JsonResponse
import datetime


# Create your views here.

def menu(request):
    items = Item.objects.all()
    template = loader.get_template('customer/menu.html')
    context = {
        'items': items,
    }
    return render(request, 'customer/menu.html', context)


def order(request):
    items = Item.objects.all()
    stocklevel = ItemStockLevels.objects.all()

    # creating a formset
    OrderFormSet = formset_factory(OrderForm, extra=10)
    formset = OrderFormSet(request.POST or None, initial=0)

    if formset.is_valid():
        new_id = random.randint(1000, 9999)
        counter = 1
        neworder = Orders(new_id, datetime.date.today(), request.user.username, request.user.id, False)
        neworder.save()
        for form in formset:
            quantity = form.cleaned_data.get('item_quantity', 0)
            custor = CustomerOrders(counter * new_id, new_id, counter, quantity)
            custor.save()
            counter = counter + 1
        context = {
            'new_id': new_id,
        }

        send_mail('Order number ' + str(new_id) + ' at Frankie\'s Italian Cuisine has been confirmed',
                  'Your order with order number ' + str(new_id) + ' at Frankie\'s Italian Cuisine has been confirmed.',
                  None,
                  [request.user.email],
                  )

        return render(request, "customer/order_confirmed.html", context)

    # Add the formset to context dictionary
    context = {
        'items': items,
        'formset': formset,
    }
    return render(request, "customer/order.html", context)


def acctdet(request):
    custid = request.user.id
    orders = Orders.objects.all().filter(custid=custid)
    context = {
        'orders': orders,
    }
    return render(request, "customer/account_details.html", context)


@staff_member_required
def inventory(request):
    form = IngredientForm(request.POST or None, initial=None)
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


@staff_member_required
def activeorder(request):
    orders = Orders.objects.all().filter(complete=False)
    items = CustomerOrders.objects.all()
    form = PushOrder(request.POST or None)
    user = get_user_model()
    template = loader.get_template('inventory/active_orders.html')
    if form.is_valid():
        sendorder=form.cleaned_data.get('orderid')
        orderupd = Orders.objects.get(order=sendorder)
        orderupd.complete = True
        orderupd.save()

        useremail = user.objects.get(id=Orders.objects.get(order=sendorder).custid).email

        send_mail('Order number ' + str(sendorder) + ' at Frankie\'s Italian Cuisine is ready for pickup!',
                  'Your order with order number ' + str(sendorder) + ' at Frankie\'s Italian Cuisine is now ready for pickup.',
                  None,
                  [useremail],
                  )

        context = {
            'orders': orders,
            'form': form,
        }
        return render(request, 'inventory/active_orders.html', context)
    context = {
        'orders': orders,
        'form': form,
    }
    return render(request, 'inventory/active_orders.html', context)


@staff_member_required
def suppman(request):
    form = RestockForm(request.POST or None)
    instocks = Ingredients.objects.all()
    ingredients = ItemStockLevels.objects.all()
    template = loader.get_template('inventory/suppman.html')
    if form.is_valid():
        ing = ItemStockLevels.objects.get(ingredient_name=form.cleaned_data.get('name'))
        ing.quantity = ing.quantity + form.cleaned_data.get('quantity')
        ing.restock_date = datetime.date.today()
        ing.save()
        context = {
            'ingredients': ingredients,
            'instocks': instocks,
            'form': form,
        }
        return render(request, 'inventory/suppman.html', context)
    context = {
        'ingredients': ingredients,
        'instocks': instocks,
        'form': form,
    }
    return render(request, 'inventory/suppman.html', context)


@staff_member_required
def sales(request):
    labels = []
    data = []

    template = loader.get_template('inventory/sales.html')

    qs = CustomerOrders.objects.all()

    for customer_order in qs:
        labels.append(customer_order.menu_item_id)
        data.append(customer_order.quantity)

    return render(request, 'inventory/sales.html', {
        'labels': labels,
        'data': data,
    })
