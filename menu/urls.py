from django.urls import path
from .views import*

app_name = 'menu'

urlpatterns = [
    path('', FoodListView.as_view(), name='menu'),
    path('<str:slug>/', DetailFoodView.as_view(), name='detail')
]
