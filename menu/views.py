from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Pizza, Drinks, Sauces, LatestFood


class GeneralView(View):

    def get(self, request, *args, **kwargs):
        food = LatestFood.object.get_food_for_main_page('pizza', 'sauces')
        return render(request, 'menu/menu.html', {'food': food})


class PizzaListView(ListView):
    model = Pizza
    template_name = "menu/pizza.html"

    def get_queryset(self):
        return Pizza.objects.select_related('composition')


class DrinksListView(ListView):
    model = Drinks
    template_name = 'menu/drinks.html'


class SaucesListView(ListView):
    model = Sauces
    template_name = 'menu/sauces.html'


class DetailPizzaView(DetailView):
    model = Pizza
    template_name = 'menu/pizza_detail.html'


class DetailDrinkView(DetailView):
    model = Drinks
    template_name = 'menu/drink_detail.html'


class DetailSauceView(DetailView):
    model = Sauces
    template_name = 'menu/sauce_detail.html'
