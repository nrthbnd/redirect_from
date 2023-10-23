import re

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_api_get_url(urlmap):
    """Проверка наличия запрашиваемой короткой ссылки."""
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)


def validate_api_body(data):
    """Проверка наличия тела запроса."""
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса', 400)


def validate_api_data_url(data):
    """Проверка наличия поля с оригинальной ссылкой."""
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', 400)


def validate_api_short_link(data):
    """Проверка корректности создания короткой ссылки."""
    pattern = r'^[A-Za-z0-9_]{1,16}$'
    if not re.match(pattern, data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.', 400)
