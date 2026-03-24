from datetime import date, timedelta
import socket, qrcode, psutil
from my_bar.settings import BAR_PRICE
from cocktails.models import Cocktail, Ingridient, Client, Ingridient_Cost, Bill, Taste, Alcohol, Group
import sqlite3
from django.shortcuts import get_object_or_404, redirect, render

def get_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    bills = show_bills(request)
    not_aval_set = get_available()
    tastes = Taste.objects.all()
    alco = Alcohol.objects.all()
    groups = Group.objects.all()
    client = Client.objects.get(user=request.user)
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).order_by('name')
    text = 'Ваш фильтр: '
    if request.method == 'GET':
        if request.GET.get('taste_id'):
            cocks = cocks.filter(taste_id=request.GET.get('taste_id'))
            text += str(Taste.objects.filter(id=request.GET.get('taste_id'))[0]) + ' '
        if request.GET.get('alco_id'):
            cocks = cocks.filter(alcohol_id=request.GET.get('alco_id'))
            text += str(Alcohol.objects.filter(id=request.GET.get('alco_id'))[0]) + ' '
        if request.GET.get('group_id'):
            cocks = cocks.filter(group_id=request.GET.get('group_id'))
            text += str(Group.objects.filter(id=request.GET.get('group_id'))[0])
    context = {
        'cocks': cocks,
        'bills': bills,
        'tastes': tastes,
        'client': client,
        'alco': alco,
        'groups': groups,
        'text': text,
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
    return redirect('index')

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
    bills = show_bills(request)
    context = {
        'bills': bills,
    }
    return render(request, 'cocktails/rules.html', context=context)

def show_wishlist(request):
    bills = show_bills(request)
    context = {
        'bills': bills,
    }
    wishlist = Ingridient.objects.all().filter(availability=False).filter(category__in=[1, 2])
    context = {
        'wishlist': wishlist,
        'bills': bills,
    }
    return render(request, 'cocktails/wishlist.html', context=context)

def get_qr(request):
    bills = show_bills(request)
    addrs = psutil.net_if_addrs()
    for ad in addrs.get('Беспроводная сеть'):
        if ad.family == socket.AF_INET:
            host = ad.address + ':8000'
    image = qrcode.make(host)
    image.save('media/qr/qrcode.png')
    context = {
        'host': host,
        'bills': bills,
    }
    return render(request, 'cocktails/qr.html', context=context)