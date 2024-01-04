from django.contrib import admin
from .models import Ingridient, Cocktail, Category, Alcohol, Taste, Group, Clients, Ingridient_Cost, Bill

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CocktailAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'group', 'img', 'alcohol_perc', 'method')
    list_editable = ('cost', 'group', 'img', 'method')

class IngridientdAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'availability', 'cost', 'alcohol_perc')
    list_editable = ('availability', 'cost', 'alcohol_perc')

class AlcoholAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TasteAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    list_editable = ('balance',)

class Ingridient_CostAdmin(admin.ModelAdmin):
    list_display = ('ingridient_id', 'cocktail_id', 'value')
    list_editable = ('value',)

class BillAdmin(admin.ModelAdmin):
    list_display = ('cock_name', 'timestamp', 'client', 'cost')

admin.site.register(Ingridient, IngridientdAdmin)
admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Alcohol, AlcoholAdmin)
admin.site.register(Taste, TasteAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Ingridient_Cost, Ingridient_CostAdmin)
admin.site.register(Bill, BillAdmin)