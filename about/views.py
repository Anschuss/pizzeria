from django.views.generic import ListView
from .models import InfoPizzeria


class InfoPizzeria(ListView):
    model = InfoPizzeria
    template_name = 'about/about.html'

