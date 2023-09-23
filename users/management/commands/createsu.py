# images/management/commands/createsu.py

from users.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@mail.com').exists():
            User.objects.create_superuser(
                email='admin@mail.com',
                password='password'
            )
        print('Superuser has been created.')