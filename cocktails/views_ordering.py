import sqlite3
from datetime import datetime
from math import floor

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from cocktails.views import show_bills
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render

from cocktails.models import Client, Cocktail, Ingridient_Cost, Ingridient, Bill


def order(request, cocktail_id):
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        cock = Cocktail.objects.all().get(id=cocktail_id)
        ingrids = Ingridient_Cost.objects.filter(cocktail_id=cocktail_id)
        for i in ingrids:
            Ingridient.objects.filter(id=i.ingridient_id.id).update(count=i.ingridient_id.count - i.value)
            if int(Ingridient.objects.get(id=i.ingridient_id.id).count) <= 0:
                Ingridient.objects.filter(id=i.ingridient_id.id).update(availability=False)
        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()
        sqlite_insert_query = f"""INSERT INTO cocktails_bill
                              (timestamp, cock_name, client, cost, is_done, is_canceled, is_cock)
                              VALUES
                              ('{datetime.now()}', '{cock.name}', '{client.name}', {cock.cost}, False, False, True);"""
        client.balance -= cock.cost
        client.save()

        cursor.execute(sqlite_insert_query)
        connect.commit()
        connect.close()
    return redirect('index')

@staff_member_required
def mark_completed(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.is_done = True
    bill.save(update_fields=["is_done"])
    messages.success(request, f"Заказ '{bill.cock_name}' помечен как выполненный.")
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def mark_canceled(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.is_canceled = True
    bill.save(update_fields=["is_canceled"])
    if bill.is_cock is True:
        cocktail = get_object_or_404(Cocktail, name=bill.cock_name)
        ingridients = get_list_or_404(Ingridient_Cost, cocktail_id=cocktail.pk)
        for i in ingridients:
            ingridient = get_object_or_404(Ingridient, id=i.ingridient_id.pk)
            ingridient.count += i.value
            if ingridient.count > 0:
                ingridient.availability = True
            ingridient.save()


    else:
        ingridient = get_object_or_404(Ingridient, name=bill.cock_name)
        ingridient.count += bill.value
        if ingridient.count > 0:
            ingridient.availability = True
        ingridient.save()
    client = get_object_or_404(Client, name=bill.client)
    client.balance += bill.cost
    client.save()
    messages.success(request, f"Заказ '{bill.cock_name}' помечен как отмененный.")
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def just_drink(request):
    bills = show_bills(request)
    drinks = Ingridient.objects.filter(category__in=[1, 2]).filter(availability=True)
    context = {
        'drinks': drinks,
        'bills': bills,
    }
    return render(request, 'cocktails/just_drink.html', context)


def order_drink(request):
    if request.method == 'POST':
        drink_id = request.POST.get("drink")
        value = request.POST.get("value")
        client = Client.objects.get(user=request.user)
        drink = Ingridient.objects.get(id=drink_id)
        cost = floor(drink.cost / 500 * int(value))

        Ingridient.objects.filter(id=drink_id).update(count=drink.count - int(value))
        if int(Ingridient.objects.get(id=drink_id).count) <= 0:
            Ingridient.objects.filter(id=drink_id).update(availability=False)

        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()
        sqlite_insert_query = f"""INSERT INTO cocktails_bill
                              (timestamp, cock_name, client, cost, is_done, is_canceled, is_cock, value)
                              VALUES
                              ('{datetime.now()}', '{drink.name}', '{client.name}', {cost}, False, False, False, {value});"""
        client.balance -= cost
        client.save()

        cursor.execute(sqlite_insert_query)
        connect.commit()
        connect.close()
    return redirect('index')
