from django.contrib import admin
from catalog.models import Product, Category, ContactFormMessage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_product', 'category', 'purchase_price',)
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



