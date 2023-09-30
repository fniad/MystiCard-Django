from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_publish

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create_article'),
    path('', cache_page(60)(BlogListView.as_view()), name='list_articles'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view_article'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_article'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_article'),
    path('toggle_publish/<int:pk>/', toggle_publish, name='toggle_publish'),
]
