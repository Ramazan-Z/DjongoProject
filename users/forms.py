from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "country",
            "password1",
            "password2",
        )

    def clean_phone_number(self) -> Any:
        """Валидация номера телефона"""
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер должен состоять только из цыфр")
        return phone_number

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Добавление стилей в инициализацию"""
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
