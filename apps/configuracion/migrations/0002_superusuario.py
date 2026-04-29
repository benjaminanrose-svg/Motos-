from django.db import migrations


def crear_superusuario(apps, schema_editor):
    from django.contrib.auth.models import User
    user = User.objects.first()
    if user:
        user.set_password('Keloke2024!')
        user.is_staff = True
        user.is_superuser = True
        user.save()
    else:
        User.objects.create_superuser('keloke', '', 'Keloke2024!')


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_superusuario, migrations.RunPython.noop),
    ]
