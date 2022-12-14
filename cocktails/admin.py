from django.contrib import admin
from .models import Ingridient, Cocktail, Category, Alcohol, Taste, Group, Clients

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CocktailAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'group')
    list_editable = ('cost', 'group')

class IngridientdAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'availability', 'cost',)
    list_editable = ('availability', 'cost',)

class AlcoholAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TasteAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    list_editable = ('balance',)

admin.site.register(Ingridient, IngridientdAdmin)
admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Alcohol, AlcoholAdmin)
admin.site.register(Taste, TasteAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Clients, ClientsAdmin)