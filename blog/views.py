from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.models import Blog
from pytils.translit import slugify
from django.utils.text import slugify


class BlogCreateView(CreateView):
    model = Blog
    fields = {'title', 'body'}
    success_url = reverse_lazy('blog:list_article')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save(commit=False)
            slug = slugify(new_article.title)
            new_article.slug = self.generate_unique_slug(slug)
            new_article.save()

        return super().form_valid(form)

    def generate_unique_slug(self, slug):
        num = 1
        new_slug = slug
        while Blog.objects.filter(slug=new_slug).exists():
            new_slug = f"{slug}-{num}"
            num += 1
        return new_slug


class BlogUpdateView(UpdateView):
    model = Blog
    fields = {'title', 'body'}

    def form_valid(self, form):
        if form.is_valid():
            updated_article = form.save(commit=False)
            if updated_article.title != form.initial['title'] or \
               updated_article.body != form.initial['body']:
                updated_article.slug = slugify(updated_article.title)
                updated_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:view_article', kwargs={'pk': self.object.pk})


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    # увеличение количества просмотров
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list_article')
