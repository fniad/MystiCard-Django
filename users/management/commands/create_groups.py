from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **options):
        # Создание группы модераторов
        moderators, created = Group.objects.get_or_create(name='moderators')
        bloggers, created = Group.objects.get_or_create(name='bloggers')
        users, created = Group.objects.get_or_create(name='users')

        moderators.is_staff = True
        moderators.save()
        bloggers.is_staff = True
        bloggers.save()

        blog_content_type = ContentType.objects.get(app_label='blog', model='blog')
        product_content_type = ContentType.objects.get(app_label='catalog', model='product')
        version_content_type = ContentType.objects.get(app_label='catalog', model='version')
        category_content_type = ContentType.objects.get(app_label='catalog', model='category')

        # продукты
        change_product = Permission.objects.get(codename='change_product', content_type=product_content_type)
        view_product = Permission.objects.get(codename='view_product', content_type=product_content_type)
        delete_product = Permission.objects.get(codename='delete_product', content_type=product_content_type)
        add_product = Permission.objects.get(codename='add_product', content_type=product_content_type)
        # версии продуктов
        change_version = Permission.objects.get(codename='change_version', content_type=version_content_type)
        view_version = Permission.objects.get(codename='view_version', content_type=version_content_type)
        add_version = Permission.objects.get(codename='add_version', content_type=version_content_type)
        delete_version = Permission.objects.get(codename='delete_version', content_type=version_content_type)
        # категории продуктов
        change_category = Permission.objects.get(codename='change_category', content_type=category_content_type)
        view_category = Permission.objects.get(codename='view_category', content_type=category_content_type)
        # статьи в блоге
        change_blog = Permission.objects.get(codename='change_blog', content_type=blog_content_type)
        add_blog = Permission.objects.get(codename='add_blog', content_type=blog_content_type)
        view_blog = Permission.objects.get(codename='view_blog', content_type=blog_content_type)
        delete_blog = Permission.objects.get(codename='delete_blog', content_type=blog_content_type)

        #
        moderators.permissions.set(
            [change_product, view_product, view_version, change_category, view_category]
        )
        bloggers.permissions.set(
            [change_blog, add_blog, delete_blog, view_blog]
        )
        users.permissions.set(
            [add_product, change_product, delete_product, view_product,
             change_version, add_version, delete_version, view_version,
             view_blog, view_category
             ]
        )

        self.stdout.write(self.style.SUCCESS('Группы успешно созданы.'))
