from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class InfoPizzerie(models.Model):
    phone_number = models.CharField(max_length=32, unique=True)
    City = models.OneToOneField(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.phone_number}, {self.City}"
