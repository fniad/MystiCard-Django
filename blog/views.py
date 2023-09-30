from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, redirect
from blog.forms import BlogForm
from blog.models import Blog
from django.utils import timezone


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.add_blog'
    success_url = reverse_lazy('blog:list_articles')

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


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse_lazy('blog:view_article', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            updated_article = form.save(commit=False)
            if updated_article.title != form.initial['title'] or \
               updated_article.body != form.initial['body']:
                updated_article.slug = slugify(updated_article.title)
                updated_article.slug = self.generate_unique_slug(updated_article.slug)
                updated_article.save()

        return super().form_valid(form)

    def generate_unique_slug(self, slug):
        num = 1
        new_slug = slug
        while Blog.objects.filter(slug=new_slug).exists():
            new_slug = f"{slug}-{num}"
            num += 1
        return new_slug


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    # увеличение количества просмотров
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'blog.delete_article'
    success_url = reverse_lazy('blog:list_articles')


@login_required
def toggle_publish(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.is_published = not blog.is_published
    blog.date_published = timezone.now()
    blog.save()
    return redirect('blog:view_article', pk=pk)
