from django import template
from django.conf import settings

register = template.Library()


# <img src="{{ object.image|mediapath }}" />
@register.filter
def mediapath(filepath):
    return f"{settings.MEDIA_URL}{filepath}"