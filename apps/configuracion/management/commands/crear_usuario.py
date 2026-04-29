from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea el usuario del taller si no existe ninguno'

    def handle(self, *args, **options):
        if User.objects.exists():
            self.stdout.write('Ya existe un usuario, no se creó ninguno.')
            return

        User.objects.create_superuser(
            username='keloke',
            email='',
            password='Keloke2024!',
        )
        self.stdout.write(self.style.SUCCESS(
            'Usuario creado — user: keloke / pass: Keloke2024!'
        ))
