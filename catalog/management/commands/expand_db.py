from django.core import serializers
from django.core.management import BaseCommand
from itertools import chain

from catalog.models import Category, Product, Version, ContactFormMessage
from blog.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        models = [Category, Product, Post, Version, ContactFormMessage]

        with open('fixtures/data.json', 'w') as file:
            data = serializers.serialize('json', chain(*[model.objects.all() for model in models]))
            file.write(data)