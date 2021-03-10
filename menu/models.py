import hashlib
from django.db import models


class Types(models.Model):
    """ Types of food """
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        slug = hashlib.sha1(self.name.encode('utf-8'))
        self.slug = slug.hexdigest()
        super(Types, self).save(**kwargs)


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
    slug = models.SlugField(unique=True)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self, **kwargs):
        slug = hashlib.sha1(self.name.encode('utf-8'))
        self.slug = slug.hexdigest()
        super(Product, self).save(**kwargs)


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
