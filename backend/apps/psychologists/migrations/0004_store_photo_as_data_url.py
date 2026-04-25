# Generated manually to store psychologist photos directly in the database.

import base64
import mimetypes
from pathlib import Path

from django.conf import settings
from django.db import migrations, models


def file_path_to_data_url(path_value):
    path_value = str(path_value or '')
    if not path_value or path_value.startswith('data:image/'):
        return path_value

    file_path = Path(settings.MEDIA_ROOT) / path_value
    if not file_path.exists() or not file_path.is_file():
        return ''

    content_type = mimetypes.guess_type(file_path.name)[0] or 'image/jpeg'
    encoded = base64.b64encode(file_path.read_bytes()).decode('ascii')
    return f'data:{content_type};base64,{encoded}'


def convert_existing_photos(apps, schema_editor):
    PsychologistProfile = apps.get_model('psychologists', 'PsychologistProfile')
    for profile in PsychologistProfile.objects.exclude(photo=''):
        new_photo = file_path_to_data_url(profile.photo)
        if new_photo != profile.photo:
            profile.photo = new_photo
            profile.save(update_fields=['photo'])


class Migration(migrations.Migration):

    dependencies = [
        ('psychologists', '0003_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "UPDATE psychologist_profiles SET photo = '' WHERE photo IS NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name='psychologistprofile',
            name='photo',
            field=models.TextField(
                blank=True,
                default='',
                help_text='Base64 data URL with the psychologist profile photo.',
                verbose_name='profile photo image',
            ),
        ),
        migrations.RunPython(
            convert_existing_photos,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
