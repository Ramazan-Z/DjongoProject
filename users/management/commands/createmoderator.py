import os
from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Создание пользователя с правами модератора"

    def handle(self, *args: Any, **options: Any) -> None:
        user = CustomUser.objects.create(
            email=os.getenv("MODERATOR_EMAIL"),
            username=os.getenv("MODERATOR_USERNAME"),
        )
        user.set_password(os.getenv("MODERATOR_PASSWORD"))
        moderators_group = Group.objects.get(name="Moderators")
        user.groups.add(moderators_group)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully created moderator user with email {user.email}"))
