from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    help = 'Добавляем в соответствующие группы модератора и ответственного за блог'

    def handle(self, *args, **options):
        moderator = User.objects.create(
            email='manager-mysticard@yandex.ru',
            first_name='Moderator',
            last_name='MystiCard',
            is_staff=True,
            is_superuser=False,
        )

        blogger = User.objects.create(
            email='content-manager-mysticard@yandex.ru',
            first_name='Content-manager',
            last_name='MystiCard-blog',
            is_staff=True,
            is_superuser=False,
        )

        moderator.groups.add(Group.objects.get(name='moderators'))
        blogger.groups.add(Group.objects.get(name='bloggers'))

        moderator.set_password('moderator1234')
        moderator.save()
        blogger.set_password('content1234')
        blogger.save()

        self.stdout.write(self.style.SUCCESS('Контент-менеджер блога и модератор успешно добавлены.'))
