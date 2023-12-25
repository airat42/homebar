from django.shortcuts import render, get_object_or_404
from cocktails.models import Cocktail, Ingridient, Clients, Ingridient_Cost
import sqlite3

wish = [68, 69, 59, 3, 4, 8, 24, 31, 53, 57, 47, 52, 2, 10, 12, 14, 41, 23, 63, 16, 29, 17, 9, 15, 45, 46, 61, 66, 26, 33]
def get_unique_numbers(numbers):
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return unique

queryset1 = Clients.objects.raw('SELECT * FROM cocktails_clients WHERE balance <> 0 ORDER BY balance')

def get_queryset(request):
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).order_by('name')
    context = {
        'cocks': cocks
    }

    # ingr_list = []
    # connect = sqlite3.connect('db.sqlite3')
    # cursor = connect.cursor()
    # for cock in aval:
    #     final_cost = 0
    #     cursor.execute(f"SELECT cocktails_ingridient_cost.id FROM cocktails_ingridient_cost JOIN cocktails_cocktail ON cocktails_ingridient_cost.cocktail_id_id=cocktails_cocktail.id WHERE cocktails_cocktail.name='{cock}'")
    #     ingridients_ids = cursor.fetchall()
    #     for i in ingridients_ids:
    #         ingridient_final = get_object_or_404(Ingridient_Cost, pk=i[0])
    #         ingr_list.append(ingridient_final)
    #         final_cost += int((ingridient_final.ingridient_id.cost / 500) * ingridient_final.value)
    #         Cocktail.objects.filter(name=cock).update(cost=round(final_cost*1.1))
    # connect.close()

    return render(request, 'cocktails/index.html', context=context)

def get_available():
    not_aval = []
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    cursor.execute(
        f"SELECT cocktails_ingridient_cost.cocktail_id_id FROM cocktails_ingridient_cost JOIN cocktails_ingridient ON cocktails_ingridient_cost.ingridient_id_id=cocktails_ingridient.id WHERE cocktails_ingridient.availability is False")
    not_aval_cocks = cursor.fetchall()
    connect.close()
    for cock in not_aval_cocks:
        not_aval.append(cock[0])
    not_aval_set = set(not_aval)
    return not_aval_set


# def get_context_data(object_list=None, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['queryset1'] = queryset1
#     return context

def show_category(request, taste_id):
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).filter(taste_id=taste_id).order_by('name')

    context = {
        'cocks': cocks,
        'taste_id': taste_id,
    }
    return render(request, 'cocktails/taste.html', context=context)

def show_cocktail(request, cocktail_id):
    cocktail = get_object_or_404(Cocktail, pk=cocktail_id)
    ingr_list = []
    final_cost = 0
    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM cocktails_ingridient_cost WHERE cocktail_id_id={cocktail_id}")
    ingridients_ids = cursor.fetchall()
    connect.close()
    for i in ingridients_ids:
        ingridient_final = get_object_or_404(Ingridient_Cost, pk=i[0])
        ingr_list.append(ingridient_final)
        final_cost += int((ingridient_final.ingridient_id.cost / 500) * ingridient_final.value)
    context = {
        'cocktail': cocktail,
        'title': cocktail.name,
        'ingr_list': ingr_list,
        'final_cost': round(final_cost * 1.1)
    }

    return render(request, 'cocktails/cocktail.html', context=context)

def show_rules(request):
    return render(request, 'cocktails/rules.html')

def show_wishlist(request):
    wishlist = Ingridient.objects.all().filter(availability=False).filter(id__in=wish).filter(category__in=[1, 2, 3])
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'cocktails/wishlist.html', context=context)

def show_alcohol(request, alcohol_id):
    not_aval_set = get_available()
    cocks = Cocktail.objects.all().exclude(id__in=not_aval_set).order_by('name').filter(alcohol_id=alcohol_id)

    context = {
        'cocks': cocks,
        'alcohol_id': alcohol_id
    }
    return render(request, 'cocktails/alcohol.html', context=context)