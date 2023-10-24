import re
from http import HTTPStatus

from settings import REGEX_PATTERN

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_api_get_url(urlmap):
    """Проверка наличия запрашиваемой короткой ссылки."""
    if urlmap is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND)


def validate_api_body(data):
    """Проверка наличия тела запроса."""
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST)


def validate_api_data_url(data):
    """Проверка наличия поля с оригинальной ссылкой."""
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST)


def validate_api_short_link(data):
    """Проверка корректности создания короткой ссылки."""
    if not re.match(REGEX_PATTERN, data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.',
            HTTPStatus.BAD_REQUEST)
