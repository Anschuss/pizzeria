from django.contrib import admin
from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'composition', 'price', 'slug')
    fields = ['name', 'price', 'img', 'composition', 'description', 'weight']


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'slug')
    fields = ['name', 'size', 'price', 'img']

class SaucesAdmin(admin.ModelAdmin):
    list_display = ('name', 'composition', 'price', 'slug')
    fields = ['name', 'composition', 'size']


admin.site.register(CompositionDish)
admin.site.register(Food, FoodAdmin)
admin.site.register(Drinks, DrinkAdmin)
admin.site.register(Sauces, SaucesAdmin)
