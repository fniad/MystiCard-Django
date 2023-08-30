from django.core.management import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product, ContactFormMessage, Version


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        ContactFormMessage.objects.all().delete()
        Version.objects.all().delete()

        call_command('loaddata', 'fixtures/data.json')
