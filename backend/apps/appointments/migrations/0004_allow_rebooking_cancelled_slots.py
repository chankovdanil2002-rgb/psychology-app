# Создана вручную: позволяет повторно бронировать отменённые слоты.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_initial'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_slot',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='appointments',
                to='schedule.timeslot',
                verbose_name='time slot',
            ),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(
                condition=models.Q(('status__in', ['pending', 'confirmed'])),
                fields=('time_slot',),
                name='unique_active_appointment_per_time_slot',
            ),
        ),
    ]
