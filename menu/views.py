from django.views.generic import ListView
from .models import Food


class FoodListView(ListView):
    model = Food
    template_name = "menu/menu.html"

    def get_queryset(self):
        return Food.objects.select_related('composition')

