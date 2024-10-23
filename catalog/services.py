from typing import Any

from django.core.cache import cache
from django.db.models.query import QuerySet

from catalog.models import Category, Product
from config.settings import CACH_ENABLED


class ProductServices:
    """Класс вспомогательных функций товаров"""

    @staticmethod
    def check_cache(queryset: Any) -> Any:
        """Проверяет queryset в кэше, возвращает его или оригинал"""
        if CACH_ENABLED:
            cached_queryset = cache.get("queryset")
            if cached_queryset:
                return cached_queryset
            cache.set("queryset", queryset, 5 * 60)
        return queryset


class CategoriesServices:
    """Класс вспомогательных функций категорий товаров"""

    @staticmethod
    def get_current_category() -> Any:
        """Получает текущую категорию из кэша или категорию по умолчанию"""
        cached_current_category = cache.get("current_category")
        if cached_current_category:
            return cached_current_category
        return CategoriesServices.set_current_category()

    @staticmethod
    def set_current_category(category_name: str | None = None) -> Category:
        """Сохраняет в кэш текущую категорию или первую из списка категорий"""
        if category_name:
            current_category = Category.objects.get(title=category_name)
        else:
            current_category = list(Category.objects.all())[0]
        cache.set("current_category", current_category)
        return current_category

    @staticmethod
    def get_categories() -> QuerySet:
        """Получение набора категорий"""
        return Category.objects.all()

    @staticmethod
    def get_queryset() -> Any:
        """Получение набора товаров для отображения"""
        return Product.objects.filter(category=CategoriesServices.get_current_category())
