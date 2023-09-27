from django.contrib import admin
from catalog.models import Product, Category, ContactFormMessage, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_product', 'category', 'purchase_price', 'is_published')
    list_filter = ('archive', 'category',)
    search_fields = ('name_product', 'description_product',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_category',)
    search_fields = ('name_category',)


@admin.register(ContactFormMessage)
class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message', 'data_sent')
    search_fields = ('name', 'phone', 'email',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'version_number',)
    search_fields = ('product',)



