from django.db import models
from django.db.models.query import QuerySet
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name



class RestaurantMenuItemQuerySet(models.QuerySet):
    def get_restaurants_by_order(self, order_id):
        order = Order.objects.select_related('restaurant').get(pk=order_id)
        if order.restaurant:
            return {order.restaurant}

        product_ids = order.items.all().values_list('product_id', flat=True)
        restaurants = Restaurant.objects.filter(
            menu_items__product_id__in=product_ids,
            menu_items__availability=True
        ).distinct()

        restaurants = restaurants.filter(menu_items__product_id__in=product_ids)

        return restaurants.distinct()


class RestaurantMenuItem(models.Model):
    available = RestaurantMenuItemQuerySet.as_manager()
    objects = models.Manager()
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
    ('PR', 'Обработанный'),
    ('UN', 'Необработанный'),
    ]
    PAYMENT_CHOICES = [
    ('CASH', 'Наличными'),
    ('CARD', 'Электронно'),
    ('NS', 'Не указано'),
    ]
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='orders',
        verbose_name='ресторан',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=2,
        choices=STATUS_CHOICES ,
        default="UN",
    )
    payment_method = models.CharField(
        verbose_name='Способ оплаты',
        max_length=4,
        choices=PAYMENT_CHOICES ,
        default="NS",
    )
    firstname = models.CharField(
        verbose_name='Имя',
        max_length=50,
    )
    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
    )
    address = models.CharField(
        verbose_name='Адрес доставки',
        max_length=50,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
    )
    products = models.ManyToManyField(
        Product,
        verbose_name='продукты',
        through='OrderItem',
        related_name='orders'
    )
    comment = models.TextField(
        verbose_name='комментарий к заказу',
        max_length=200,
        blank=True,
    )
    registered_at = models.DateTimeField(
        verbose_name='дата создания',
        default=timezone.now)
    

    called_at = models.DateTimeField(
        verbose_name='дата обзванивания',
        default=timezone.now,
        blank=True,
        null=True)
    

    delivered_at = models.DateTimeField(
        verbose_name='дата доставки',
        blank=True,
        null=True
        )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name='заказ',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    

    class Meta:
        verbose_name = 'продукт в заказе'
        verbose_name_plural = 'продукты в заказе'

    def __str__(self):
        return f'{self.product.name} в заказе {self.order.id}'
    

    
    

