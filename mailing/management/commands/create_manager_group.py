from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу Manager'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Менеджеры')

        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана"))
