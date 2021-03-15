from django.contrib import admin
from .models import InfoPizzeria, UserMessage


class InfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone_number_pizzeria')


admin.site.register(InfoPizzeria, InfoAdmin),
admin.site.register(UserMessage)
