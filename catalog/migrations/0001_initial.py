# Generated by Django 4.2.3 on 2023-08-06 14:39

from django.db import migrations, models


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
                ('data_sent', models.CharField(verbose_name='дата сообщения')),
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
                ('category', models.CharField(max_length=50, verbose_name='категория')),
                ('purchase_price', models.FloatField(verbose_name='цена за покупку')),
                ('date_create', models.DateField(default='2023-08-06', verbose_name='дата создания')),
                ('date_last_modified', models.DateField(verbose_name='дата последнего изменения')),
                ('archive', models.BooleanField(default=False, verbose_name='архивный')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'ordering': ('pk',),
            },
        ),
    ]
