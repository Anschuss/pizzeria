from django.urls import path
from .views import FoodListView

app_name = 'menu'

urlpatterns = [
    path('', FoodListView.as_view(), name='menu'),
]
