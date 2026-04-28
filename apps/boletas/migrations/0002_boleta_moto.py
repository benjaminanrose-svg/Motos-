import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boletas', '0001_initial'),
        ('clientes', '0002_moto'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleta',
            name='moto',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='boletas',
                to='clientes.moto',
            ),
        ),
    ]
