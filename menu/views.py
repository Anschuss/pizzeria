from django.views.generic import ListView, DetailView
from .models import Food, Drinks


class FoodListView(ListView):
    model = Food
    template_name = "menu/menu.html"

    def get_queryset(self):
        return Food.objects.select_related('composition')


class DetailFoodView(DetailView):
    model = Food
    template_name = 'menu/pizza.html'


class DrinksListView(ListView):
    model = Drinks
    template_name = 'menu/drinks.html'


class DetailDrinkView(DetailView):
    model = Drinks
    template_name = 'menu/drink.html'
