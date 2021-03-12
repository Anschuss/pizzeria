from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('', FoodListView.as_view(), name='menu'),
    path('drinks/', DrinksListView.as_view(), name='drinks'),
    path('<str:slug>/', DetailFoodView.as_view(), name='detail'),
    path('drinks/<str:slug>/', DetailDrinkView.as_view(), name='detail_drink'),
]
