from django.shortcuts import render
from catalog.models import Product
from datetime import datetime
from catalog.models import ContactFormMessage, Category
from django.core.paginator import Paginator


def index(request):

    products_list = Product.objects.all()
    paginator = Paginator(products_list, 6)  # Показывать 10 элементов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'object_list': products_list,
        'title': 'Главная',
        'page_obj': page_obj
    }

    return render(request, 'catalog/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data_sent = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'You have new message in from {name}({phone} {email}): {message}')

        # Создание объекта ContactFormMessage и сохранение в базе данных
        contact_message = ContactFormMessage(name=name, phone=phone, email=email, message=message, data_sent=data_sent)
        contact_message.save()

    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contact.html', context)


def product_info(request):
    context = {
        'title': 'Товар'
    }
    return render(request, 'catalog/product_info.html', context)


def courses(request):
    context = {
        'title': 'Курсы'
    }
    return render(request, 'catalog/courses.html', context)


def add_product(request):
    if request.method == 'POST':
        name_product = request.POST.get('name_product')
        description_product = request.POST.get('description_product')
        preview_img = 'null'
        category_pk = request.POST.get('category')  # Идентификатор категории
        purchase_price = request.POST.get('purchase_price')
        date_create = datetime.now().strftime('%Y-%m-%d')
        date_last_modified = date_create
        archive = False

        category = Category.objects.get(pk=category_pk)  # Получить объект категории по идентификатору

        # Создание объекта Product и сохранение в базе данных
        add_new_product = Product(
            name_product=name_product,
            description_product=description_product,
            preview_img=preview_img,
            category=category,
            purchase_price=purchase_price,
            date_create=date_create,
            date_last_modified=date_last_modified,
            archive=archive
        )
        add_new_product.save()

    categories = Category.objects.all()

    context = {
        'title': 'Добавить продукт',
        'categories': categories
    }

    return render(request, 'catalog/add_product.html', context)

