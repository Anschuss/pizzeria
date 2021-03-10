from django.contrib import admin
from .models import *


class TypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    fields = ['name']


admin.site.register(Types, TypesAdmin)
admin.site.register(CompositionDish)
admin.site.register(Food)
admin.site.register(Drinks)
admin.site.register(Sauces)
