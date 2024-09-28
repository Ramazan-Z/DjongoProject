from django.db import models


class BlogEntry(models.Model):
    """Класс-модель сущности блоговой записи"""

    # Заголовок
    heading: models.Field = models.CharField(max_length=200, verbose_name="Заголовок", help_text="Введите заголовок")
    # Содержимое
    content: models.Field = models.TextField(
        verbose_name="Содержимое", blank=True, null=True, help_text="Введите содержимое"
    )
    # Превью
    preview: models.Field = models.ImageField(
        upload_to="blog/images/", verbose_name="Превью", blank=True, null=True, help_text="Загрузите изображение"
    )
    # Дата создания
    created_at: models.Field = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # Признак публикации
    is_publication: models.Field = models.BooleanField(blank=True, default=False)
    # Количество просмотров
    view_counter: models.Field = models.IntegerField(verbose_name="Количество просмотров", blank=True, default=0)

    def __str__(self) -> str:
        """Строковое представление записи"""
        return str(self.heading)

    class Meta:
        """Метаданные модели"""

        db_table = "blog_entry"  # Имя таблицы в БД
        verbose_name = "Запись"  # Отображаемое имя в ед. числе
        verbose_name_plural = "Записи"  # Отображаемое имя во мн. числе
        ordering = ["heading"]  # Порядок сортировки
