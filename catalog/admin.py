from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели категорий в админке"""

    list_display = ("id", "title")
    search_fields = ("title", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Регистрация модели товаров в админке"""

    list_display = ("id", "title", "price", "category")
    list_filter = ("category",)
    search_fields = ("title", "description")
