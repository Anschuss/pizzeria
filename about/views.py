from django.views.generic import ListView, FormView, TemplateView, \
    CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InfoPizzeria, UserMessage
from .froms import *


class InfoPizzeriaView(ListView):
    model = InfoPizzeria
    template_name = 'about/about.html'


class DeliveryAndPaymentView(TemplateView):
    template_name = 'about/delivery_and_payment.html'


class ContactView(LoginRequiredMixin, FormView):
    template_name = 'about/message.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        message = form.cleaned_data['message']

        message = UserMessage(email=email, phone_number=phone_number, message=message)
        message.save()

        return super().form_valid(form)


## USER

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView


class CreateUserView(CreateView):
    model = User
    form_class = RegistrationUserForm
    success_url = '/'
    template_name = 'about/registration.html'


class LoginUserView(LoginView):
    form_class = LoginUserForm
    success_url = '/'
    template_name = 'about/login.html'


class LogoutUser(LogoutView):
    pass
