"""Вспомогательные функции для хранения изображений профиля в формате base64."""
import base64
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError
from rest_framework import serializers


MAX_PROFILE_IMAGE_SIZE = 5 * 1024 * 1024
PROFILE_IMAGE_MAX_SIDE = 512
PROFILE_IMAGE_QUALITY = 85


def image_bytes_to_data_url(image_bytes):
    """Преобразует байты изображения в компактный JPEG data URL."""
    try:
        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)
    except UnidentifiedImageError as exc:
        raise serializers.ValidationError(
            'Загрузите корректное изображение.'
        ) from exc

    image.thumbnail((PROFILE_IMAGE_MAX_SIDE, PROFILE_IMAGE_MAX_SIDE))
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    output = BytesIO()
    image.save(
        output,
        format='JPEG',
        quality=PROFILE_IMAGE_QUALITY,
        optimize=True,
    )
    encoded = base64.b64encode(output.getvalue()).decode('ascii')
    return f'data:image/jpeg;base64,{encoded}'


def uploaded_image_to_data_url(uploaded_file):
    """Конвертирует загруженный файл изображения в base64 data URL для браузера."""
    content_type = getattr(uploaded_file, 'content_type', '') or ''
    if not content_type.startswith('image/'):
        raise serializers.ValidationError(
            'Загрузите изображение в формате JPG, PNG, GIF или WEBP.'
        )

    if uploaded_file.size > MAX_PROFILE_IMAGE_SIZE:
        raise serializers.ValidationError(
            'Размер изображения не должен превышать 5 МБ.'
        )

    image_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    return image_bytes_to_data_url(image_bytes)
