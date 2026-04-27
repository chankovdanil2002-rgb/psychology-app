# Создана вручную: компактирует аватары клиентов, хранящиеся в базе данных.

import base64
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.db import migrations
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_SIDE = 512
JPEG_QUALITY = 85


def value_to_image_bytes(value):
    value = str(value or '')
    if not value:
        return b''

    if value.startswith('data:image/') and ',' in value:
        return base64.b64decode(value.split(',', 1)[1])

    file_path = Path(settings.MEDIA_ROOT) / value
    if file_path.exists() and file_path.is_file():
        return file_path.read_bytes()

    return b''


def compact_image_value(value):
    image_bytes = value_to_image_bytes(value)
    if not image_bytes:
        return ''

    try:
        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)
    except (UnidentifiedImageError, OSError):
        return ''

    image.thumbnail((MAX_SIDE, MAX_SIDE))
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    output = BytesIO()
    image.save(output, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    encoded = base64.b64encode(output.getvalue()).decode('ascii')
    return f'data:image/jpeg;base64,{encoded}'


def compact_existing_avatars(apps, schema_editor):
    ClientProfile = apps.get_model('clients', 'ClientProfile')
    for profile in ClientProfile.objects.exclude(avatar=''):
        new_avatar = compact_image_value(profile.avatar)
        if new_avatar != profile.avatar:
            profile.avatar = new_avatar
            profile.save(update_fields=['avatar'])


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_store_avatar_as_data_url'),
    ]

    operations = [
        migrations.RunPython(
            compact_existing_avatars,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
