from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Resetea la contraseña del usuario del taller'

    def handle(self, *args, **options):
        user = User.objects.first()
        if user:
            user.set_password('Keloke2024!')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'OK — usuario: {user.username} / pass: Keloke2024!'
            ))
        else:
            User.objects.create_superuser('keloke', '', 'Keloke2024!')
            self.stdout.write(self.style.SUCCESS(
                'OK — usuario: keloke / pass: Keloke2024!'
            ))
