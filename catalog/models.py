from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name_category = models.CharField(max_length=150, verbose_name='категория')
    description_category = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name_category}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name_category',)


class Product(models.Model):
    name_product = models.CharField(max_length=150, verbose_name='продукт')
    description_product = models.TextField(verbose_name='описание')
    preview_img = models.ImageField(upload_to='products/', verbose_name='изображение превью', ** NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    purchase_price = models.FloatField(verbose_name='цена за покупку')
    date_create = models.DateField(verbose_name='дата создания', default=timezone.now)
    date_last_modified = models.DateField(verbose_name='дата последнего изменения')
    date_published = models.DateField(verbose_name='дата публикации', default=None, **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='опубликован')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, ** NULLABLE, verbose_name='владелец')

    archive = models.BooleanField(default=False, verbose_name='архивный')

    def __str__(self):
        return f'{self.name_product} {self.category} {self.purchase_price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('pk',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт', ** NULLABLE)
    version_number = models.PositiveIntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=100, verbose_name='название версии', ** NULLABLE)
    is_current = models.BooleanField(verbose_name='признак версии', default=False)

    def __str__(self):
        return f'{self.product} - Версия {self.version_number}: {self.version_name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class ContactFormMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    email = models.EmailField(verbose_name='email')
    message = models.TextField(verbose_name='сообщение')
    data_sent = models.CharField(max_length=30, verbose_name='дата сообщения')

    def __str__(self):
        return f'У вас сообщение от {self.name}({self.phone} {self.email}): {self.message}'

    class Meta:
        verbose_name = 'сообщение с контактной формы'
        verbose_name_plural = 'сообщения с контактной формы'
