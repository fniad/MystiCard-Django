# Generated by Django 4.2.3 on 2023-09-03 16:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_category', models.CharField(max_length=150, verbose_name='категория')),
                ('description_category', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name_category',),
            },
        ),
        migrations.CreateModel(
            name='ContactFormMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='имя')),
                ('phone', models.CharField(max_length=20, verbose_name='телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('message', models.TextField(verbose_name='сообщение')),
                ('data_sent', models.CharField(max_length=30, verbose_name='дата сообщения')),
            ],
            options={
                'verbose_name': 'сообщение с контактной формы',
                'verbose_name_plural': 'сообщения с контактной формы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_product', models.CharField(max_length=150, verbose_name='продукт')),
                ('description_product', models.TextField(verbose_name='описание')),
                ('preview_img', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='изображение превью')),
                ('purchase_price', models.FloatField(verbose_name='цена за покупку')),
                ('date_create', models.DateField(default=django.utils.timezone.now, verbose_name='дата создания')),
                ('date_last_modified', models.DateField(verbose_name='дата последнего изменения')),
                ('archive', models.BooleanField(default=False, verbose_name='архивный')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField(verbose_name='номер версии')),
                ('version_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='название версии')),
                ('is_current', models.BooleanField(default=False, verbose_name='признак версии')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
    ]
