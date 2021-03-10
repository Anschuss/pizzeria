from django.views.generic import ListView, DetailView
from .models import Food


class FoodListView(ListView):
    model = Food
    template_name = "menu/menu.html"

    def get_queryset(self):
        return Food.objects.select_related('composition')


class DetailFoodView(DetailView):
    pass
