from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Дает группе Manager perms: просмотр всех клиентов, рассылок'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        perms = [
            'can_view_all_recipients',
            'can_view_all_messages',
            'can_view_all_broadcasts',
            'broadcast_shutdown',
            'view_users_list'
        ]

        for perm in perms:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' получила: view права на клиентов, сообщения, рассылки,"
                                             "остановки рассылки и списка пользователей сервиса"))
