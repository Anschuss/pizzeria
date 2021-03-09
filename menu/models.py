from django.db import models


class Types(models.Model):
    """ Types of food """
    name = models.CharField(max_length=64, unique=True)


class CompositionDish(models.Model):
    text = models.TextField


class Food(models.Model):
    name = models.CharField(max_length=120, unique=True)
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    price = models.PositiveIntegerField()
    weight = models.FloatField()


class Drinks(models.Model):
    name = models.CharField(max_length=64, unique=True)
    size = models.FloatField()
    price = models.PositiveIntegerField()


class Sauces(models.Model):
    name = models.CharField(max_length=64)
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    size = models.FloatField(default=95.5)
    price = models.PositiveIntegerField()
