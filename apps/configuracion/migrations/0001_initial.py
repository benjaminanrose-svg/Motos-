from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ConfiguracionTaller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Keloke', max_length=150)),
                ('rut', models.CharField(blank=True, max_length=15)),
                ('direccion', models.CharField(blank=True, max_length=255)),
                ('telefono', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('horario', models.CharField(blank=True, help_text='Ej: Lun–Vie 9:00–18:30 / Sáb 9:00–14:00', max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='taller/')),
                ('mensaje_pie_boleta', models.CharField(blank=True, default='¡Gracias por su preferencia!', max_length=255)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Configuración del Taller',
                'verbose_name_plural': 'Configuración del Taller',
            },
        ),
    ]
