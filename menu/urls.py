from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
    path('food/<str:ct_model>/<str:slug>/', FoodDetailView.as_view(), name='food_detail'),
    path('category/<str:ct_model>/<str:slug>/', CategoryDetailView.as_view(), name='category_detail')
    # path('add_to_cart/<str:ct_model>/<str:slug>/', AddCartView.as_view(), name='add_to_cart')
]
