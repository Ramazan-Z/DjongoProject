from typing import Any

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Clear test data from data base"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Удаляем существующие записи"""
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("The data has been successfully deleted from the database"))
