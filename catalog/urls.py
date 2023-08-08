from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
]
