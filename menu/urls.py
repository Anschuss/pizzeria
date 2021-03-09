from django.urls import path
from .views import FoodListView

app_name = 'menu'

urlpatterns = [
    path('all_menu/', FoodListView.as_view(), name='menu'),
]
