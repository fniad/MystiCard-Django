from datetime import datetime

from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import ContactFormMessage, Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    paginate_by = 6

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_product')

    def get_success_url(self):
        return reverse('catalog:edit_product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST)
        else:
            formset = VersionFormset()

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.date_create = timezone.now().date()
            self.object.date_last_modified = timezone.now().date()
            self.object.owner = self.request.user

            formset.instance = self.object
            self.object.save()
            formset.save()

            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:edit_product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if form.is_valid() and formset.is_valid():
            new_product = form.save(commit=False)
            if new_product.name_product != form.initial['name_product'] or \
                    new_product.purchase_price != form.initial['purchase_price']:
                new_product.date_last_modified = timezone.now().date()
            new_product.save()

            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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
