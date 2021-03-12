from django.urls import path
from .views import InfoPizzeria

app_name = 'about'

urlpatterns = [
    path('us/', InfoPizzeria.as_view(), name='about'),
]
