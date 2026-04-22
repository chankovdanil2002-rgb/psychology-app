"""
Вспомогательные функции: кастомный обработчик исключений и хелперы стандартных ответов.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений DRF, оборачивающий все ответы об ошибках
    в единый формат:

        {
            "status": "error",
            "message": "Краткое описание для человека",
            "data": { ... detail или ошибки полей ... }
        }
    """
    response = exception_handler(exc, context)

    if response is None:
        # Необработанное исключение — возвращаем обобщённый ответ 500.
        return Response(
            {
                'status': 'error',
                'message': 'An unexpected error occurred.',
                'data': {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Формируем читаемое сообщение из данных ответа.
    error_data = response.data

    if isinstance(error_data, dict):
        # Если есть ключ верхнего уровня 'detail' — используем его как сообщение.
        if 'detail' in error_data:
            message = str(error_data.pop('detail'))
            data = error_data
        else:
            # Собираем сообщения об ошибках полей.
            messages = []
            for field, errors in error_data.items():
                if isinstance(errors, list):
                    for err in errors:
                        messages.append(f'{field}: {err}')
                else:
                    messages.append(f'{field}: {errors}')
            message = '; '.join(messages) if messages else 'Validation error.'
            data = error_data
    elif isinstance(error_data, list):
        message = '; '.join(str(e) for e in error_data)
        data = {'errors': error_data}
    else:
        message = str(error_data)
        data = {}

    response.data = {
        'status': 'error',
        'message': message,
        'data': data,
    }

    return response


def success_response(data=None, message='', status_code=status.HTTP_200_OK):
    """
    Возвращает стандартизированный успешный ответ.

    Args:
        data: Сериализованные данные для тела ответа.
        message: Читаемое сообщение об успехе.
        status_code: HTTP-код статуса (по умолчанию 200).

    Returns:
        DRF Response в формате:
        {
            "status": "success",
            "message": "...",
            "data": { ... }
        }
    """
    return Response(
        {
            'status': 'success',
            'message': message,
            'data': data if data is not None else {},
        },
        status=status_code,
    )
