from django.db import transaction
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Pizza, Drinks, Sauces, \
    LatestFood, CartFood, Cart, Customer, Category
from .mixins import CartMixin, CategoryDetailMixin
from .utils import recalc_cart
from .forms import OrderForm


class GeneralView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        food = LatestFood.object.get_food_for_main_page('pizza', 'sauces')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, ListView):
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
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        food = LatestFood.object.get_food_for_main_page(kwargs['ct_model'])
        return render(request, 'menu/category_detail.html', {'food': food})


class AddCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, food_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        food = content_type.model_class().objects.get(slug=food_slug)
        cart_food, created = CartFood.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=food.id
        )
        if created:
            self.cart.food.add(cart_food)
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, food_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        food = content_type.model_class().objects.get(slug=food_slug)
        cart_food, created = CartFood.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=food.id
        )
        self.cart.food.remove(cart_food)
        cart_food.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, food_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        food = content_type.model_class().objects.get(slug=food_slug)
        cart_food, created = CartFood.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=food.id
        )
        qty = int(request.POST.get('qty'))
        cart_food.qty = qty
        cart_food.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'menu/cart.html', context)


class CheckoutView(CartView, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
        }
        return render(request, 'menu/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone_number']
            new_order.address = form.cleaned_data['address']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
