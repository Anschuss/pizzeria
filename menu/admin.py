from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'model_name')
    fields = ['name', 'model_name']


class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'composition', 'price', 'category', 'slug')
    fields = ['name', 'price', 'img', 'category', 'composition', 'description', 'weight']


class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'slug')
    fields = ['name', 'size', 'category', 'price', 'img']


class SaucesAdmin(admin.ModelAdmin):
    list_display = ('name', 'composition', 'category', 'price', 'slug')
    fields = ['name', 'size', 'price', 'category', 'composition', 'img']


admin.site.register(Cart)
admin.site.register(CartFood)
admin.site.register(Customer)
admin.site.register(CompositionDish)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Drinks, DrinkAdmin)
admin.site.register(Sauces, SaucesAdmin)
admin.site.register(Category, CategoryAdmin)
