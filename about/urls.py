from django.urls import path
from .views import *

app_name = 'about'

urlpatterns = [
    path('us/', InfoPizzeriaView.as_view(), name='about'),
    path('delivery_and_payment/', DeliveryAndPaymentView.as_view(), name='delivery_and_payment'),
    path('contact/', ContactView.as_view(), name='contact'),
    ## User
    path('registration/', CreateUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout')
]
