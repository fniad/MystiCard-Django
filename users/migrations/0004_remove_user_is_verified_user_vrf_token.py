# Generated by Django 4.2.3 on 2023-09-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='vrf_token',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='токен'),
        ),
    ]
