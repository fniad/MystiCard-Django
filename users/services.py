from django.core.mail import send_mail
import random
import string
from config import settings


def generate_new_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))


def generate_vrf_token():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))


def send_hello_and_confirm_url(confirm_url, email):
    send_mail(
        subject='Поздравляем с регистрацией на сайте MailMagic',
        message=f'Пожалуйста, подтвердите свою электронную почту по ссылке {confirm_url}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_password(email, new_password):
    send_mail(
        subject='Вы сменили пароль на сайте MailMagic',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
