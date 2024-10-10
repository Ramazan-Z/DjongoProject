from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Класс формы продукта"""

    class Meta:
        """Метаданные формы"""

        model = Product
        exclude = ["created_at", "updated_at"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Добавление стилей в инициализацию"""
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                        "placeholder": field.help_text,
                    }
                )
                field.help_text = ""

    def clean_price(self) -> Any:
        """Валидация цены"""
        price = self.cleaned_data.get("price", 0)
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean(self) -> Any:
        """ "Защита от спама"""
        cleaned_data = super().clean()
        title = cleaned_data.get("title", "") if cleaned_data else ""
        description = cleaned_data.get("description", "") if cleaned_data else ""

        for word in FORBIDDEN_WORDS:
            if word.lower() in title.lower():
                self.add_error("title", f"Слово {word} запещено!")
            if word.lower() in description.lower():
                self.add_error("description", f"Слово {word} запещено!")
