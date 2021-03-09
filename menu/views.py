from django.shortcuts import render
from django.views.generic import ListView
from .models import Food


class FoodListView(ListView):
    model = Food
    template_name = ""
