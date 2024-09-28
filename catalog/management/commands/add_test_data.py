from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """Загрузка тестовых данных из фикстур"""
        call_command("clear_db")
        call_command("loaddata", "category_fixture.json")
        call_command("loaddata", "product_fixture.json")
        call_command("loaddata", "blog_entries_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
