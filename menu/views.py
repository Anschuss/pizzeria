from django.views.generic import ListView, DetailView
from .models import Food, Drinks, Sauces


class FoodListView(ListView):
    model = Food
    template_name = "menu/menu.html"

    def get_queryset(self):
        return Food.objects.select_related('composition')


class DrinksListView(ListView):
    model = Drinks
    template_name = 'menu/drinks.html'


class SaucesListView(ListView):
    model = Sauces
    template_name = 'menu/sauces.html'


class DetailFoodView(DetailView):
    model = Food
    template_name = 'menu/pizza_detail.html'


class DetailDrinkView(DetailView):
    model = Drinks
    template_name = 'menu/drink_detail.html'


class DetailSauceView(DetailView):
    model = Sauces
    template_name = 'menu/sauce_detail.html'
