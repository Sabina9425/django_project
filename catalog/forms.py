from django.forms import ModelForm, forms, BooleanField

from catalog.models import Product, Version


class StyleFormMixIn:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


def check_cleaned_data(cleaned_data):
    if any(word in cleaned_data for word in
           ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]):
        raise forms.ValidationError("Введены недопустимые слова. Пожалуйста, повторите ввод")


class ProductForm(ModelForm):

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        check_cleaned_data(cleaned_data)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        check_cleaned_data(cleaned_data)
        return cleaned_data

    class Meta:
        model = Product
        fields = "__all__"
        exclude =("owner",)


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
