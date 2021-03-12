from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
    path('pizza/', PizzaListView.as_view(), name='pizza'),
    path('drinks/', DrinksListView.as_view(), name='drinks'),
    path('sauces/', SaucesListView.as_view(), name='sauces'),
    path('pizza/<str:slug>/', DetailPizzaView.as_view(), name='detail'),
    path('drinks/<str:slug>/', DetailDrinkView.as_view(), name='detail_drink'),
    path('sauces/<str:slug>/', DetailSauceView.as_view(), name='detail_sauce')
]
