from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
    path('food/<str:ct_model>/<str:slug>/', FoodDetailView.as_view(), name='food_detail'),
    path('category/<str:ct_model>/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    # path('pizza/', PizzaListView.as_view(), name='pizza'),
    # path('drinks/', DrinksListView.as_view(), name='drinks'),
    # path('sauces/', SaucesListView.as_view(), name='sauces'),
    # path('pizza/<str:ct_model>/<str:slug>/', DetailPizzaView.as_view(), name='detail'),
    # path('drinks/<str:ct_model>/<str:slug>/', DetailDrinkView.as_view(), name='detail_drink'),
    # path('sauces/<str:slug>/', DetailSauceView.as_view(), name='detail_sauce'),
    # path('cart/', CartView.as_view(), name='cart'),
    # path('add_to_cart/<str:ct_model>/<str:slug>/', AddCartView.as_view(), name='add_to_cart')
]
