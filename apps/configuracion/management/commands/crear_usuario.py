from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Elimina todos los usuarios y crea uno nuevo limpio'

    def handle(self, *args, **options):
        User.objects.all().delete()
        User.objects.create_superuser('keloke', '', 'Keloke2024!')
        self.stdout.write(self.style.SUCCESS(
            'Listo — usuario: keloke / pass: Keloke2024!'
        ))
