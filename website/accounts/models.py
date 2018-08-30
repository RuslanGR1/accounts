from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.


class Group(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групы'

    def __str__(self):
        return self.title


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code


class AccountType(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField('Категория', max_length=30)
    description = models.CharField('Описание', max_length=200)
    price = models.DecimalField('За 1 шт.', decimal_places=2, max_digits=7, default=0)

    def get_short_description(self):
        if len(self.description) > 50:
            return '%s..' % self.description[:50]
        return self.description

    def get_count(self):
        return Account.objects.filter(type=self, is_active=True).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория аккаунта'
        verbose_name_plural = 'Категории аккаунтов'


class Order(models.Model):
    METHOD_CHOICE = (
        ('QIWI', 'Qiwi'),
    )
    type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=METHOD_CHOICE, default='QIWI')
    count = models.PositiveIntegerField('Кол-во', validators=[MinValueValidator(1)])
    pay_comment = models.CharField('Qiwi примечание', max_length=20)
    paid = models.BooleanField('Оплачен', default=False)
    complete = models.BooleanField('Аккаунты выданы', default=False)
    email = models.EmailField(default=None)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    download_code = models.CharField(max_length=30, default=None, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', related_name='orders', null=True, blank=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        self.total_price = self.count * self.type.price
        if self.coupon and self.coupon.active:
            self.total_price = self.total_price - self.total_price * (self.coupon.discount / Decimal('100'))
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.created.strftime("%A, %d. %B %Y %I:%M%p")


class Account(models.Model):
    type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, null=True, blank=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)  # Еще не продан - True

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.login
