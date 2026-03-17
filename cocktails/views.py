from datetime import datetime, date, timedelta
from math import floor
from tkinter.font import names

from forms import CreateForm
from my_bar.settings import BAR_PRICE
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from cocktails.models import Cocktail, Ingridient, Client, Ingridient_Cost, Bill, Taste, Alcohol
import sqlite3
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

wish = [68, 69, 59, 3, 4, 8, 24, 31, 53, 57, 47, 52, 2, 10, 12, 14, 41, 23, 63, 16, 29, 17, 9, 15, 45, 46, 61, 66, 26, 33]
def get_unique_numbers(numbers):
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return unique

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Такой пользователь уже существует!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        Client.objects.create(user=user, name=username, balance=0)
        login(request, user)
        return redirect('index')

    return render(request, 'cocktails/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль!')
            return redirect('login')

    return render(request, 'cocktails/login.html')


def logout_view(request):
    response = redirect('login')  # после выхода отправляем на страницу логина
    logout(request)

    # Сбрасываем все cookies (кроме служебных Django)
    for key in request.COOKIES:
        response.delete_cookie(key)

    messages.success(request, "Вы успешно вышли из системы.")
    return response


def get_queryset(request):
    if not request.user.is_authenticated:
        return redirect('login')
    bills = show_bills(request)
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).order_by('name')
    tastes = Taste.objects.all()
    alco = Alcohol.objects.all()
    client = Client.objects.get(user=request.user)
    context = {
        'cocks': cocks,
        'bills': bills,
        'tastes': tastes,
        'client': client,
        'alco': alco,
    }
    return render(request, 'cocktails/index.html', context=context)

def refresh_cock(request):
    cocks = Cocktail.objects.all().order_by('name')
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    for cock in cocks:
        final_cost = 0
        litres = 0
        final_perc = 0
        cursor.execute(
            f"SELECT cocktails_ingridient_cost.id FROM cocktails_ingridient_cost "
            f"JOIN cocktails_cocktail ON cocktails_ingridient_cost.cocktail_id_id=cocktails_cocktail.id "
            f"WHERE cocktails_cocktail.name='{cock}'")
        ingridients_ids = cursor.fetchall()
        for i in ingridients_ids:
            ingridient_final = get_object_or_404(Ingridient_Cost, pk=i[0])
            final_cost += int((ingridient_final.ingridient_id.cost / 500) * ingridient_final.value)
            litres += int(ingridient_final.value)
            final_perc += int(ingridient_final.ingridient_id.alcohol_perc * ingridient_final.value)
        final_alcohol = final_perc / litres
        Cocktail.objects.filter(name=cock).update(cost=round(final_cost * BAR_PRICE))
        Cocktail.objects.filter(name=cock).update(alcohol_perc=round(final_alcohol))
    connect.close()
    return redirect(f'http://127.0.0.1:8000/')


def get_available():
    not_aval = []
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    cursor.execute(
        f"SELECT cocktails_ingridient_cost.cocktail_id_id FROM cocktails_ingridient_cost "
        f"JOIN cocktails_ingridient ON cocktails_ingridient_cost.ingridient_id_id=cocktails_ingridient.id "
        f"WHERE cocktails_ingridient.availability is False OR cocktails_ingridient_cost.value > cocktails_ingridient.count")
    not_aval_cocks = cursor.fetchall()
    connect.close()
    for cock in not_aval_cocks:
        not_aval.append(cock[0])
    not_aval_set = set(not_aval)
    return not_aval_set

def show_category(request, taste_id):
    bills = show_bills(request)
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).filter(taste_id=taste_id).order_by('name')
    client = Client.objects.get(user=request.user)
    context = {
        'cocks': cocks,
        'taste_id': taste_id,
        'bills': bills,
        'client': client,
    }
    return render(request, 'cocktails/taste.html', context=context)

def show_cocktail(request, pk):
    bills = show_bills(request)
    cocktail = get_object_or_404(Cocktail, pk=pk)
    ingr_list = []

    # Работа с базой
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM cocktails_ingridient_cost WHERE cocktail_id_id={pk}")
    ingridients_ids = cursor.fetchall()
    connect.close()

    for i in ingridients_ids:
        ingridient_final = get_object_or_404(Ingridient_Cost, pk=i[0])
        ingr_list.append(ingridient_final)

    context = {
        'cocktail': cocktail,
        'title': cocktail.name,
        'ingr_list': ingr_list,
        'bills': bills,
    }

    return render(request, 'cocktails/cocktail.html', context=context)


def show_bills(request):
    if not request.user.is_authenticated:
        return redirect('login')
    yesterday = str(date.today() - timedelta(days=1))
    client = Client.objects.get(user=request.user)
    if client.user.is_staff or client.user.is_superuser:
        bills = Bill.objects.filter(timestamp__gt=yesterday).order_by('timestamp')
    else:
        bills = Bill.objects.filter(timestamp__gt=yesterday, client=client).order_by('timestamp')
    return bills


def show_rules(request):
    return render(request, 'cocktails/rules.html')

def show_wishlist(request):
    wishlist = Ingridient.objects.all().filter(availability=False).filter(id__in=wish).filter(category__in=[1, 2, 3])
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'cocktails/wishlist.html', context=context)

def show_alcohol(request, alcohol_id):
    bills = show_bills(request)
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).order_by('name').filter(alcohol_id=alcohol_id)
    client = Client.objects.get(user=request.user)
    alco = Alcohol.objects.all()
    context = {
        'cocks': cocks,
        'alcohol_id': alcohol_id,
        'bills': bills,
        'client': client,
        'alco': alco,
    }
    return render(request, 'cocktails/alcohol.html', context=context)

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
    return redirect(f'http://127.0.0.1:8000')

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
    drinks = Ingridient.objects.filter(category__in=[1, 2]).filter(availability=True)
    context = {
        'drinks': drinks
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
    return redirect(f'http://127.0.0.1:8000')