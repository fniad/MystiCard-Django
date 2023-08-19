from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):

    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.SlugField(unique=True, ** NULLABLE)
    body = models.TextField(verbose_name='содержание')
    preview_img = models.ImageField(upload_to='blogs/', verbose_name='изображение превью', ** NULLABLE)
    date_create = models.DateField(verbose_name='дата создания', default=timezone.now)

    is_published = models.BooleanField(default=True, verbose_name='опубликован')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title} {self.slug}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('pk',)
