from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Pizza, Drinks, Sauces, LatestFood, CartFood, Cart, Customer
from .mixins import CartMixin
from .utils import recalc_cart


class GeneralView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        food = LatestFood.object.get_food_for_main_page('pizza', 'sauces')
        context = {
            'food': food,
            'cart': self.cart,
        }
        return render(request, 'menu/menu.html', context)


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


class AddCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, food_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        food = content_type.model_class().objects.get(slug=food_slug)
        cart_food, created = CartFood.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=food.id
        )
        if created:
            self.cart.food.add()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin,View):

    def get(self, request, *args, **kwargs):
        return render(request, 'menu/cart.html', {'cart': self.cart})
