from flask import jsonify, request
from http import HTTPStatus

from settings import LOCAL_HOST
from . import app, db
from .api_validators import (validate_api_get_url, validate_api_body,
                             validate_api_data_url, validate_api_short_link)
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_link>/', methods=['GET'])
def get_urlmap(short_link):
    """Получить оригинальную ссылку по указанному короткому идентификатору."""
    urlmap = URLMap.query.filter_by(short=short_link).first()
    validate_api_get_url(urlmap)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    """Cоздать новую короткую ссылку."""
    data = request.get_json()
    validate_api_body(data)
    validate_api_data_url(data)
    if (
        'custom_id' not in data or
        data['custom_id'] is None or
        data['custom_id'] == ''
    ):
        data['custom_id'] = get_unique_short_id()

    validate_api_short_link(data)

    new_link = URLMap()
    new_link.from_dict(data)
    db.session.add(new_link)
    db.session.commit()
    return jsonify(
        short_link=LOCAL_HOST + data['custom_id'],
        url=new_link.to_dict()['url']
    ), HTTPStatus.CREATED
