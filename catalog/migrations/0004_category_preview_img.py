# Generated by Django 4.2.5 on 2023-09-30 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product_date_published_product_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='preview_img',
            field=models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='изображение категории'),
        ),
    ]
