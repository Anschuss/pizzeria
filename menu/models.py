import hashlib
from django.db import models


class Types(models.Model):
    """ Types of food """
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def slug_generate(self):
        slug = hashlib.sha1(self.name)
        self.slug = slug.hexdigest()


class CompositionDish(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Product(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=120, unique=True)
    price = models.PositiveIntegerField()
    img = models.TextField()
    slug = models.SlugField()

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def slug_generate(self):
        slug = hashlib.sha1(self.name)
        self.slug = slug.hexdigest()


class Food(Product):
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    weight = models.FloatField()

    def __str__(self):
        return self.name


class Drinks(Product):
    size = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.price}"


class Sauces(Product):
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    size = models.FloatField(default=95.5)

    def __str__(self):
        return f"{self.name}, {self.price}"
