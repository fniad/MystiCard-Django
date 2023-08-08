from django.shortcuts import render
from catalog.models import Product
from datetime import datetime
from catalog.models import ContactFormMessage


def index(request):

    last_five_products = Product.objects.order_by('date_create')[:5]
    for product in last_five_products:
        print(product.name_product)  # Вывод в консоль названия последних 5 товаров

    context = {
        # 'object_list': student_list,
        'title': 'Главная',
        'last_five_products': last_five_products
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
