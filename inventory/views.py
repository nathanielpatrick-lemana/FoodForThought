from django.shortcuts import render
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db import connection

from .models import Item
from .models import Ingredients
from .models import ItemStockLevels
from .models import CustomerOrders
from .models import Orders
from .forms import OrderForm
from .forms import IngredientForm
from .forms import RestockForm
from .forms import PushOrder
from .forms import CardForm
from account.forms import AcctDetUpdateForm
import random
from django.forms import formset_factory
from django.core.mail import send_mail
from django.http import JsonResponse
import datetime
import numpy as np


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
    modelformset = formset_factory(OrderForm, extra=10)
    formset = modelformset(request.POST or None, initial=0)
    cardform = CardForm(request.POST or None)

    if formset.is_valid() and cardform.is_valid():
        # fix this and think of a new way of giving orders ids
        cardno = str(cardform.cleaned_data.get('card_number'))[-4:]
        new_id = random.randrange(0, 99999)
        counter = 1
        items = []

        neworder = Orders(new_id, datetime.date.today(), request.user.username, request.user.id, False, True, 0.00)
        neworder.save()
        total = 0
        for form in formset:
            quantity = form.cleaned_data.get('quantity', 0)
            if quantity == 0:
                counter = counter + 1
                continue
            custor = CustomerOrders(counter * new_id, new_id, counter, quantity)
            custor.save()
            getprice_cur = connection.cursor()
            getprice_cur.execute("SELECT inventory_item.price FROM inventory_item WHERE inventory_item.id = " + str(counter) + ";")
            add = getprice_cur.fetchall()
            total = total + (add[0][0]*quantity)
            counter = counter + 1
        neworder.total = total
        neworder.save()
        cursor = connection.cursor()
        # update the stock history here
        order_id = neworder.order
        # get the results of the consumption query
        cursor.execute("SELECT inventory_ingredients.name, SUM(inventory_recipeitem.quantity) * inventory_customerorders.quantity as 'aggregated' FROM inventory_ingredients, inventory_item, inventory_recipeitem, inventory_customerorders, inventory_orders WHERE inventory_orders.order = {} AND inventory_customerorders.order_id_id = inventory_orders.order AND inventory_customerorders.menu_item_id_id = inventory_recipeitem.menu_item_id_id AND inventory_recipeitem.ingredient_id_id = inventory_ingredients.ingredient GROUP BY inventory_ingredients.name;".format(order_id))
        # loop over tuple to capture the name of ingredients
        ingredient_names = [item[0] for item in cursor.fetchall()]
        cursor.execute("SELECT inventory_ingredients.name, SUM(inventory_recipeitem.quantity) * inventory_customerorders.quantity as 'aggregated' FROM inventory_ingredients, inventory_item, inventory_recipeitem, inventory_customerorders, inventory_orders WHERE inventory_orders.order = {} AND inventory_customerorders.order_id_id = inventory_orders.order AND inventory_customerorders.menu_item_id_id = inventory_recipeitem.menu_item_id_id AND inventory_recipeitem.ingredient_id_id = inventory_ingredients.ingredient GROUP BY inventory_ingredients.name;".format(order_id))
        ingredient_amounts = [item[1] for item in custor.fetchall()]
        # run cursor execute update query based on the ingredient name
        for i in range(len(ingredient_names)):
            # using the ingredient name in list use an sql query to get the current stock level
            cursor.execute("SELECT inventory_itemstocklevels.quantity FROM inventory_itemstocklevels WHERE inventory_itemstocklevels.ingredient_name = {ingredient_names[i]};")
            item_stock_result = cursor.fetchall()

            # get the ingredient id
            cursor.execute(
                "SELECT inventory_itemstocklevels.ingredient_id_id FROM inventory_itemstocklevels WHERE inventory_itemstocklevels.ingredient_name = {ingredient_names[i]};")
            ingredient_id = cursor.fetchall()
            ingredient_id = str(ingredient_id[0][0])
            ingredient_id = int(ingredient_id)

            # store that result and subtract the corresponding ingredient amount
            item_stock_result = item_stock_result - ingredient_amounts[i]

            # that resulting amount will be updated in item stock levels and given a new row in stock history
            cursor.execute("UPDATE inventory_itemstocklevels SET inventory_itemstocklevels.quantity = {item_stock_result} WHERE inventory_itemstocklevels.ingredient_id_id = {ingredient_id};")

            # insert new record into stock history
            today = datetime.date.today()
            cursor.execute("INSERT INTO inventory_stockhistory VALUES ('{today}', item_stock_result, ingredient_id);")

        cursor.execute("SELECT inventory_item.name, inventory_customerorders.quantity FROM inventory_customerorders, inventory_item WHERE inventory_customerorders.order_id_id =" + str(new_id) + " AND inventory_item.id = inventory_customerorders.menu_item_id_id;")
        results = cursor.fetchall()
        send_mail('Order number ' + str(new_id) + ' at Frankie\'s Italian Cuisine has been confirmed',
                  'Your order with order number ' + str(new_id) + ' at Frankie\'s Italian Cuisine has been confirmed. '
                                                                  'Order contents: ' + str(results) + ' Order total of $' + str(total) + ' paid using the card ending in ' + cardno,
                  'Frankie\'s Italian Cuisine',
                  [request.user.email],
                  )
        context = {
            'new_id': new_id,
            'results': results,
            'total': total,
            'cardno': cardno
        }
        return render(request, "customer/order_confirmed.html", context)

    # Add the formset to context dictionary
    context = {
        'items': items,
        'formset': formset,
        'cardform': cardform,
    }
    return render(request, "customer/order.html", context)


def acctdet(request):
    custid = request.user.id
    orders = Orders.objects.all().filter(custid=custid)
    updateform = AcctDetUpdateForm(request.POST or None)
    if updateform.is_valid():
        newinfo = get_user_model().objects.all().filter(id=custid)
        newinfo.update(first_name=updateform.cleaned_data.get('first_name'),
                       last_name=updateform.cleaned_data.get('last_name'),
                       email=updateform.cleaned_data.get('email_addr'))
        context = {
            'orders': orders,
            'form': updateform,
        }
        return render(request, "customer/account_details.html", context)
    context = {
        'orders': orders,
        'form': updateform,
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
        sendorder = form.cleaned_data.get('orderid')
        orderupd = Orders.objects.get(order=sendorder)
        orderupd.complete = True
        orderupd.save()

        useremail = user.objects.get(id=Orders.objects.get(order=sendorder).custid).email

        send_mail('Order number ' + str(sendorder) + ' at Frankie\'s Italian Cuisine is ready for pickup!',
                  'Your order with order number ' + str(
                      sendorder) + ' at Frankie\'s Italian Cuisine is now ready for pickup.',
                  None,
                  [useremail],
                  )

        context = {
            'orders': orders,
            'items': items,
            'form': form,
        }
        return render(request, 'inventory/active_orders.html', context)
    context = {
        'orders': orders,
        'items': items,
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


def update_stock_history(request):
    # update every ingredient stock history for every order that is placed (STICK INSIDE ORDER FUNCTION)
    # basically insert new row after calculating
    BRUH = []


# item stock level will record the stock level of the item after every day
def item_stock_level(request):
    # this function will run when
    bruh = []


# stock history will be recorded every day and will hold the stock level after every day of business
def stock_consumption(request):
    # consumption is based off the date so date of the order

    # this function should run after every order
    # make sure to compare if the order will cause negative inventory or if the order will make inventory trip the restock (i.e hit or go under restock level)
    # if the order causes restock then run item stock level
    bruh = []


# add in charts for daily, weekly and monthly revenue
# charts: Sales by product doughnut chart, avg daily sale, avg weekly sales, avg daily revenue, avg monthly revenue
def doughnut_chart(request):
    # SOMETHING IS WRONG WITH THIS CHART. ONLY CHEESE PIZZA WILL UPDATE BUT ALL OTHER CHARTS ARE FINE
    doughnut_menu_items = []
    sales_totals = []

    cursor = connection.cursor()
    cursor.execute(
        "SELECT inventory_item.name, SUM(inventory_customerorders.quantity) FROM inventory_item, inventory_customerorders, inventory_orders WHERE inventory_customerorders.order_id_id = inventory_orders.order AND inventory_customerorders.menu_item_id_id = inventory_item.id GROUP BY inventory_item.name")
    doughnut_menu_items = [item[0] for item in cursor.fetchall()]
    cursor.execute(
        "SELECT inventory_item.name, SUM(inventory_customerorders.quantity) FROM inventory_item, inventory_customerorders, inventory_orders WHERE inventory_customerorders.order_id_id = inventory_orders.order AND inventory_customerorders.menu_item_id_id = inventory_item.id GROUP BY inventory_item.name")
    sales_totals = [item[1] for item in cursor.fetchall()]

    return JsonResponse(data={
        'labels': doughnut_menu_items,
        'data': sales_totals,
    })


def average_daily_sales(request):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT inventory_item.name, avg(inventory_customerorders.quantity) AS 'avg sales' FROM inventory_orders, inventory_customerorders, inventory_item WHERE inventory_orders.order = inventory_customerorders.order_id_id AND inventory_item.id = inventory_customerorders.menu_item_id_id GROUP BY inventory_item.name;")
        menu_items = [item[0] for item in cursor.fetchall()]
        cursor.execute(
            "SELECT inventory_item.name, avg(inventory_customerorders.quantity) AS 'avg sales' FROM inventory_orders, inventory_customerorders, inventory_item WHERE inventory_orders.order = inventory_customerorders.order_id_id AND inventory_item.id = inventory_customerorders.menu_item_id_id GROUP BY inventory_item.name;")
        average_daily = [item[1] for item in cursor.fetchall()]
    return JsonResponse(data={
        'labels': menu_items,
        'data': average_daily,
    })


def average_weekly_sales(request):
    # find what is the current week
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT inventory_item.name, week(inventory_orders.order_date), avg(inventory_customerorders.quantity) FROM inventory_orders, inventory_customerorders, inventory_item WHERE inventory_orders.order = inventory_customerorders.order_id_id AND inventory_item.id = inventory_customerorders.menu_item_id_id AND week(inventory_orders.order_date) > 0 GROUP BY inventory_item.name;")
        menu_items = [item[0] for item in cursor.fetchall()]
        cursor.execute(
            "SELECT inventory_item.name, week(inventory_orders.order_date), avg(inventory_customerorders.quantity) FROM inventory_orders, inventory_customerorders, inventory_item WHERE inventory_orders.order = inventory_customerorders.order_id_id AND inventory_item.id = inventory_customerorders.menu_item_id_id AND week(inventory_orders.order_date) > 0 GROUP BY inventory_item.name;")
        average_weekly = [item[2] for item in cursor.fetchall()]

        for i in range(0, np.size(average_weekly)):
            average_weekly[i] = average_weekly[i] * 7

    return JsonResponse(data={
        'labels': menu_items,
        'data': average_weekly,
    })


def aggregated_order(request, order):
    # this function will return the aggregated amounts of an order
    with connection.cursor() as cursor:
        cursor.execute(
            ""
        )


def aggregated_date(request, date):
    # this function will return the aggregated amount of leaf element items
    yp = []


def consumption(request, curr_date):
    # this function should be run every date to update the current inventory levels
    yp = []
