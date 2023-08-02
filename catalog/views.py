from django.shortcuts import render


def index(request):
    return render(request, 'catalog/index.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone} {email}): {message}')
    return render(request, 'catalog/contact.html')
