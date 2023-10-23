import re

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_api_get_url(urlmap):
    """Проверка наличия запрашиваемой короткой ссылки."""
    if urlmap is None:
        raise InvalidAPIUsage('Такой короткой ссылки не существует.', 404)


def validate_api_body(data):
    """Проверка наличия тела запроса."""
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса.')


def validate_api_data_url(data):
    """Проверка наличия поля с оригинальной ссылкой."""
    if 'url' not in data:
        raise InvalidAPIUsage(
            'В запросе отсутствует обязательное поле url.')


def validate_api_short_link(data):
    """Проверка корректности создания короткой ссылки."""
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')

    if 'custom_id' in data:
        pattern = r'^[a-zA-Z0-9]+$'
        if not re.match(pattern, data['custom_id']):
            raise InvalidAPIUsage(
                'Строка не соотвутствует шаблону [a-zA-Z0-9]{6}.')
