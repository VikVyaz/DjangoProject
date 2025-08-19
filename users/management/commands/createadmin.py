from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email=config('ADMIN_EMAIL'),
            username=config('ADMIN_USERNAME'),
        )

        user.set_password(config('ADMIN_PASSWORD'))

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f'Создан superuser с email: {user.email}'))
