from django.shortcuts import render, get_object_or_404
from cocktails.models import Cocktail, Ingridient, Clients
from django.views.generic import ListView
from itertools import chain

def get_unique_numbers(numbers):
    unique = []
    for number in numbers:
        if number not in unique:
            unique.append(number)
    return unique

queryset1 = Clients.objects.raw('SELECT * FROM cocktails_clients WHERE balance <> 0 ORDER BY balance')

class HomeView(ListView):
    model = Cocktail, Clients
    template_name = 'cocktails/index.html'

    def get_queryset(self):
        aval = []
        querysety = list(Cocktail.objects.all().values('name', 'ingridients').order_by('name'))
        querysety_1 = list(Cocktail.objects.all().filter(ingridients__availability=True).values('name', 'ingridients').order_by('name'))
        count_list = []
        my_dict = {'name': '', 'amount': 0}
        counter = 0
        namer = 'Автокатастрофа'

        for i in querysety:
            if i['name'] == namer:
                counter += 1
                my_dict.update({'name': namer, 'amount': counter})
                ss = my_dict.copy()
            elif i['name'] != namer:
                count_list.append(ss)
                namer = i['name']
                counter = 1

        count_list_1 = []
        my_dict_1 = {'name': '', 'amount': 0}
        counter_1 = 0
        namer_1 = 'Автокатастрофа'

        for i in querysety_1:
            if i['name'] == namer_1:
                counter_1 += 1
                my_dict_1.update({'name': namer_1, 'amount': counter_1})
                ss_1 = my_dict_1.copy()
            elif i['name'] != namer_1:
                count_list_1.append(ss_1)
                namer_1 = i['name']
                counter_1 = 1

        xxx = get_unique_numbers(count_list_1)

        for ch, item in enumerate(count_list):
            if count_list[ch] == xxx[ch]:
                aval.append(item['name'])

        queryset = Cocktail.objects.all().filter(name__in=aval).order_by('name')
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset1'] = queryset1
        return context

def show_category(request, taste_id):
    aval = []
    querysety = list(Cocktail.objects.all().values('name', 'ingridients').order_by('name'))
    querysety_1 = list(Cocktail.objects.all().filter(ingridients__availability=True).values('name', 'ingridients').order_by('name'))
    count_list = []
    my_dict = {'name': '', 'amount': 0}
    counter = 0
    namer = 'Автокатастрофа'

    for i in querysety:
        if i['name'] == namer:
            counter += 1
            my_dict.update({'name': namer, 'amount': counter})
            ss = my_dict.copy()
        elif i['name'] != namer:
            count_list.append(ss)
            namer = i['name']
            counter = 1

    count_list_1 = []
    my_dict_1 = {'name': '', 'amount': 0}
    counter_1 = 0
    namer_1 = 'Автокатастрофа'

    for i in querysety_1:
        if i['name'] == namer_1:
            counter_1 += 1
            my_dict_1.update({'name': namer_1, 'amount': counter_1})
            ss_1 = my_dict_1.copy()
        elif i['name'] != namer_1:
            count_list_1.append(ss_1)
            namer_1 = i['name']
            counter_1 = 1

    xxx = get_unique_numbers(count_list_1)

    for ch, item in enumerate(count_list):
        if count_list[ch] == xxx[ch]:
            aval.append(item['name'])

    cocks = Cocktail.objects.all().filter(name__in=aval).filter(taste_id=taste_id)

    context = {
        'cocks': cocks,
        'taste_id': taste_id,
    }

    return render(request, 'cocktails/taste.html', context=context)

def show_cocktail(request, cocktail_id):
    cocktail = get_object_or_404(Cocktail, pk=cocktail_id)
    context = {
        'cocktail': cocktail,
        'title': cocktail.name,
    }

    return render(request, 'cocktails/cocktail.html', context=context)

def show_rules(request):
    return render(request, 'cocktails/rules.html')

def show_wishlist(request):
    wishlist = Ingridient.objects.all().filter(availability=False).filter(category=1)
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'cocktails/wishlist.html', context=context)

def show_alcohol(request, alcohol_id):
    aval = []
    querysety = list(Cocktail.objects.all().values('name', 'ingridients').order_by('name'))
    querysety_1 = list(Cocktail.objects.all().filter(ingridients__availability=True).values('name', 'ingridients').order_by('name'))
    count_list = []
    my_dict = {'name': '', 'amount': 0}
    counter = 0
    namer = 'Автокатастрофа'

    for i in querysety:
        if i['name'] == namer:
            counter += 1
            my_dict.update({'name': namer, 'amount': counter})
            ss = my_dict.copy()
        elif i['name'] != namer:
            count_list.append(ss)
            namer = i['name']
            counter = 1

    count_list_1 = []
    my_dict_1 = {'name': '', 'amount': 0}
    counter_1 = 0
    namer_1 = 'Автокатастрофа'
    for i in querysety_1:
        if i['name'] == namer_1:
            counter_1 += 1
            my_dict_1.update({'name': namer_1, 'amount': counter_1})
            ss_1 = my_dict_1.copy()
        elif i['name'] != namer_1:
            count_list_1.append(ss_1)
            namer_1 = i['name']
            counter_1 = 1
    xxx = get_unique_numbers(count_list_1)
    for ch, item in enumerate(count_list):
        if count_list[ch] == xxx[ch]:
            aval.append(item['name'])
    cocks = Cocktail.objects.all().filter(name__in=aval).order_by('name').filter(alcohol_id=alcohol_id)
    context = {
        'cocks': cocks,
        'alcohol_id': alcohol_id,
    }
    return render(request, 'cocktails/alcohol.html', context=context)


