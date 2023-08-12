from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contact, ProductDetailView, courses, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='product_info'),
    path('courses/', courses, name='courses'),
    path('add_product/', add_product, name='add_product'),
]
