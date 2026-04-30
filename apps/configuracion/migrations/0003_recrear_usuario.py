from django.db import migrations


def recrear_superusuario(apps, schema_editor):
    from django.contrib.auth.models import User
    User.objects.all().delete()
    User.objects.create_superuser('keloke', '', 'Keloke2024!')


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0002_superusuario'),
    ]

    operations = [
        migrations.RunPython(recrear_superusuario, migrations.RunPython.noop),
    ]
