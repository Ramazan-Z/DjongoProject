from django.contrib import admin

from .models import BlogEntry


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    """Регистрация модели блоговой записи в админке"""

    list_display = ("id", "heading", "created_at", "is_publication", "view_counter")
    list_filter = ("is_publication",)
    search_fields = ("heading",)
