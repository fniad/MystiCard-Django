from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (contact, ProductDetailView, courses, ProductCreateView,
                           ProductListView, ProductUpdateView, ProductDeleteView, toggle_publish, categories,
                           ProductWithFilterListView)

app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('courses/', cache_page(60)(courses), name='courses'),
    path('', categories, name='categories'),
    path('toggle_publish/<int:pk>/', toggle_publish, name='toggle_publish'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('list_product', cache_page(60)(ProductListView.as_view()), name='list_product'),
    path('view/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='view_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('products/category/<int:category_id>/', cache_page(60)(ProductWithFilterListView.as_view()),
         name='product_list'),
]
