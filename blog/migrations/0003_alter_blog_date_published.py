# Generated by Django 4.2.3 on 2023-09-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_date_published_alter_blog_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_published',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='дата публикации'),
        ),
    ]