from django import forms
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('archive', 'date_create', 'date_last_modified', )

        widgets = {
            'is_published': forms.Select(choices=((True, 'Опубликован'), (False, 'Не опубликован'))),
        }

    def clean_name_product(self):
        cleaned_data = self.cleaned_data.get('name_product')
        restricted_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                            'полиция', 'радар']

        for word in restricted_words:
            if word in cleaned_data.lower():
                self.add_error('name_product', f'Слово "{word}" не должно находиться в названии продукта.')

        return cleaned_data

    def clean_description_product(self):
        cleaned_data = self.cleaned_data.get('description_product')
        restricted_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                            'полиция', 'радар']

        for word in restricted_words:
            if word in cleaned_data.lower():
                self.add_error('description_product', f'Слово "{word}" не должно находиться в описании продукта.')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

        widgets = {
            'is_current': forms.Select(choices=((True, 'Активная'), (False, 'Неактивная'))),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        product = cleaned_data.get('product')

        if is_current and product and Version.objects.filter(product=product, is_current=True).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError('Может быть только одна активная версия для этого продукта.')

        return cleaned_data
