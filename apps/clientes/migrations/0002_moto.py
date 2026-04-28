import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=60)),
                ('modelo', models.CharField(max_length=80)),
                ('anio', models.PositiveSmallIntegerField(verbose_name='Año')),
                ('placa', models.CharField(blank=True, max_length=10)),
                ('color', models.CharField(blank=True, max_length=40)),
                ('vin', models.CharField(blank=True, max_length=20, verbose_name='VIN / Nº Motor')),
                ('km_actual', models.PositiveIntegerField(default=0, verbose_name='Kilometraje actual')),
                ('observaciones', models.TextField(blank=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='motos',
                    to='clientes.cliente',
                )),
            ],
            options={
                'verbose_name': 'Moto',
                'verbose_name_plural': 'Motos',
                'ordering': ['marca', 'modelo'],
            },
        ),
    ]
