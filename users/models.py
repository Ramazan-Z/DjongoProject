from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="Эл. почта",
        help_text="Введите эл. почту",
    )
    avatar: models.Field = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )
    phone_number: models.Field = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    country: models.Field = models.CharField(
        max_length=60,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите страну",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]
