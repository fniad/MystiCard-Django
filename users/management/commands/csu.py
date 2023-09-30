from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создаём суперпользователя (админа)'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mistycard.com',
            first_name='Admin',
            last_name='MystiCard',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('123qwerty')
        user.save()

        self.stdout.write(self.style.SUCCESS('Суперпользователь успешно добавлен.'))