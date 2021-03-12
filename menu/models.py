import hashlib
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LatestFoodManager:

    @staticmethod
    def get_food_for_main_page(*args, **kwargs):
        food = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_food = ct_model.model_class()._base_manager.all().order_by('-id')
            food.extend(model_food)
        return food


class LatestFood:
    object = LatestFoodManager


class Types(models.Model):
    pass


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


class Pizza(Product):
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


## Order models

class CartFood(models.Model):
    # user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_food')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_objcet = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Чек:{self.content_objcet}"


class Cart(models.Model):
    # owner = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE)
    food = models.ManyToManyField(CartFood, blank=True, related_name='related_cart')
    total_food = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anomymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)
