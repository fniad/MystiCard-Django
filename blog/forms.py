from django import forms
from django.utils import timezone
from catalog.forms import StyleFormMixin
from blog.models import Blog


class BlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('preview_img', 'title', 'body', 'is_published')

        widgets = {
            'is_published': forms.Select(choices=((True, 'Публиковать'), (False, 'Черновик'))),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data['is_published']:
            instance.date_published = timezone.now()
        else:
            instance.date_published = None

        instance.date_created = timezone.now()

        if commit:
            instance.save()
        return instance