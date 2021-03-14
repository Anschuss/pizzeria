import hashlib
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


def get_model_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


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


class ClassOfClass(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self, **kwargs):
        slug = hashlib.sha1(self.name.encode('utf-8'))
        self.slug = slug.hexdigest()
        super(ClassOfClass, self).save(**kwargs)


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'pizza': 'pizza__count',
        'drinks': 'drinks__count',
        'sauces': 'sauces__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_model_for_count('pizza', 'drinks', 'sauces')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.model_name, url=f"/category/{c.model_name}/{c.slug}/",
                 count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.model_name]))
            for c in qs
        ]
        return data


class Category(ClassOfClass):
    model_name = models.CharField(max_length=32, blank=True, null=True)
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class CompositionDish(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Product(ClassOfClass):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    img = models.TextField()


class Pizza(Product):
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    weight = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:food_detail', kwargs={'ct_model': 'pizza', 'slug': self.slug})


class Drinks(Product):
    size = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.price}"

    def get_absolute_url(self):
        return reverse('menu:food_detail', kwargs={'ct_model': 'drinks', 'slug': self.slug})


class Sauces(Product):
    composition = models.OneToOneField(CompositionDish, on_delete=models.CASCADE, blank=True)
    size = models.FloatField(default=95.5)

    def __str__(self):
        return f"{self.name}, {self.price}"

    def get_absolute_url(self):
        return reverse('menu:food_detail', kwargs={'ct_model': 'sauces', 'slug': self.slug})


## Order models

class CartFood(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_food')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2)

    def __str__(self):
        return f"Чек:{self.content_object}"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE)
    food = models.ManyToManyField(CartFood, blank=True, related_name='related_cart')
    total_food = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anomymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    orders = models.ManyToManyField('Order', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    customer = models.ForeignKey(Customer, related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    order_date = models.DateField(default=timezone.now())

    def __str__(self):
        return str(self.id)
