from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Pizza, Drinks, Sauces, \
    LatestFood, CartFood, Cart, Customer, Category
from .mixins import CartMixin, CategoryDetailMixin
from .utils import recalc_cart


class GeneralView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        food = LatestFood.object.get_food_for_main_page('pizza', 'sauces')
        print(categories)
        context = {
            'categories': categories,
            'food': food,
            'cart': self.cart,
        }
        return render(request, 'menu/menu.html', context)


class FoodDetailView(CartMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'pizza': Pizza,
        'drinks': Drinks,
        'sauces': Sauces,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'food'
    template_name = 'menu/food_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'pizza': Pizza,
        'drinks': Drinks,
        'sauces': Sauces,
    }

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'menu/category_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


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


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'menu/cart.html', {'cart': self.cart})
