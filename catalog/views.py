from django.utils import timezone

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.models import ContactFormMessage
from catalog.models import Product
from pytils.translit import slugify


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products_list = Product.objects.all()
        paginator = Paginator(products_list, 6)     # Показывать 6 элементов на странице

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = {'name_product', 'description_product', 'preview_img', 'category', 'purchase_price'}
    success_url = reverse_lazy('catalog:list_product')

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.date_create = timezone.now().date()
            new_product.date_last_modified = timezone.now().date()
            new_product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = {'name_product', 'description_product', 'preview_img', 'category', 'purchase_price'}
    success_url = reverse_lazy('catalog:list_product')

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save(commit=False)
            if new_product.name_product != form.initial['name_product'] or \
                    new_product.purchase_price != form.initial['purchase_price']:
                new_product.date_last_modified = timezone.now().date()
            new_product.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list_product')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        data_sent = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Создание объекта ContactFormMessage и сохранение в базе данных
        contact_message = ContactFormMessage(name=name, phone=phone, email=email, message=message, data_sent=data_sent)
        contact_message.save()

    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contact.html', context)


def courses(request):
    context = {
        'title': 'Курсы'
    }
    return render(request, 'catalog/courses.html', context)
