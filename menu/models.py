from django.db import models


class Types(models.Model):
    """ Types of food """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class CompositionDish(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Food(models.Model):
    name = models.CharField(max_length=120, unique=True)
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    weight = models.FloatField()
    img = models.ImageField(upload_to='food', blank=True, null=True)

    def __str__(self):
        return self.name


class Drinks(models.Model):
    name = models.CharField(max_length=64, unique=True)
    size = models.FloatField()
    price = models.PositiveIntegerField()
    img = models.ImageField(upload_to='drinks', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.price}"


class Sauces(models.Model):
    name = models.CharField(max_length=64)
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    size = models.FloatField(default=95.5)
    price = models.PositiveIntegerField()
    img = models.ImageField(upload_to='sauces', blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.price}"
