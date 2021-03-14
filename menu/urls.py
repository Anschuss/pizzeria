from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('', GeneralView.as_view(), name='general'),
    path('food/<str:ct_model>/<str:slug>/', FoodDetailView.as_view(), name='food_detail'),
    path('category/<str:ct_model>/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>/', AddCartView.as_view(), name='add_to_cart'),
    path('change_qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('delete_from_cart/<str:ct_model>/<str:slug>', DeleteCartView.as_view(), name='delete_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make_order/', MakeOrderView.as_view(), name='make_order')
]
