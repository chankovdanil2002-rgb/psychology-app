from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfirmationtoken',
            name='code',
            field=models.CharField(
                blank=True,
                db_index=True,
                default='',
                max_length=6,
                verbose_name='code',
            ),
            preserve_default=False,
        ),
    ]
