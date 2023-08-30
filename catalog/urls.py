from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (contact, ProductDetailView, courses, ProductCreateView,
                           ProductListView, ProductUpdateView, ProductDeleteView)

app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('courses/', courses, name='courses'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('', ProductListView.as_view(), name='list_product'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
