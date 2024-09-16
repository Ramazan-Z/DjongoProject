from django.db import models


class Category(models.Model):
    """Класс-модель сущности категории товара"""

    # Наименование
    title: models.Field = models.CharField(
        max_length=150, unique=True, verbose_name="Наиенование", help_text="Введите наименование категории"
    )
    # Описание
    description: models.Field = models.TextField(
        verbose_name="Описание", blank=True, null=True, help_text="Введите описание категории"
    )

    def __str__(self) -> str:
        """Строковое представление категории"""
        return str(self.title)

    class Meta:
        """Метаданные модели"""

        db_table = "category"  # Имя таблицы в БД
        verbose_name = "Категория"  # Отображаемое имя в ед. числе
        verbose_name_plural = "Категории"  # Отображаемое имя во мн. числе
        ordering = ["title"]  # Порядок сортировки


class Product(models.Model):
    """Класс-модель сущности товара"""

    # Наименование
    title: models.Field = models.CharField(
        max_length=150, verbose_name="Наиенование", help_text="Введите наименование товара"
    )
    # Описание
    description: models.Field = models.TextField(
        verbose_name="Описание", blank=True, null=True, help_text="Введите описание товара"
    )
    # Изображение
    image: models.Field = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение товара",
    )
    # Категория (ForeignKey)
    category: models.Field = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    # Цена
    price: models.Field = models.IntegerField(verbose_name="Цена", help_text="Введите цену товара")
    # Дата создания
    created_at: models.Field = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # Дата последнего изменения
    updated_at: models.Field = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    def __str__(self) -> str:
        """Строковое представление товара"""
        return str(self.title)

    class Meta:
        """Метаданные модели"""

        db_table = "product"  # Имя таблицы в БД
        verbose_name = "Товар"  # Отображаемое имя в ед. числе
        verbose_name_plural = "Товары"  # Отображаемое имя во мн. числе
        ordering = ["title"]  # Порядок сортировки
