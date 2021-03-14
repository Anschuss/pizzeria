from django.db import models


class InfoPizzeria(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    email = models.CharField(max_length=32)
    phone_number_pizzeria = models.CharField(max_length=20, unique=True)
    phone_number_control = models.CharField(max_length=20, unique=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.name} {self.address} {self.email} {self.phone_number_pizzeria}'


class UserMessage(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    message = models.TextField()
