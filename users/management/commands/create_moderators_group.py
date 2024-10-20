from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создание группы с правами модератора"

    def handle(self, *args: Any, **options: Any) -> None:
        moderators_group = Group.objects.create(name="Moderators")

        del_permission = Permission.objects.get(codename="delete_product")
        unpublish_permission = Permission.objects.get(codename="can_unpublish_product")

        moderators_group.permissions.add(del_permission, unpublish_permission)
        moderators_group.save()
        self.stdout.write(self.style.SUCCESS("Successfully created moderator group"))
