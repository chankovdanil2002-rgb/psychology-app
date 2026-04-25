# Generated manually to store client avatars directly in the database.

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


def convert_existing_avatars(apps, schema_editor):
    ClientProfile = apps.get_model('clients', 'ClientProfile')
    for profile in ClientProfile.objects.exclude(avatar=''):
        new_avatar = file_path_to_data_url(profile.avatar)
        if new_avatar != profile.avatar:
            profile.avatar = new_avatar
            profile.save(update_fields=['avatar'])


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "UPDATE client_profiles SET avatar = '' WHERE avatar IS NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='avatar',
            field=models.TextField(
                blank=True,
                default='',
                help_text='Base64 data URL with the client avatar image.',
                verbose_name='avatar image',
            ),
        ),
        migrations.RunPython(
            convert_existing_avatars,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
