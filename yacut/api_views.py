from flask import jsonify, request

from . import app, db
from .api_validators import (validate_api_get_url, validate_api_body,
                             validate_api_data_url, validate_api_short_link)
from .models import URLMap


@app.route('/api/id/<string:short_link>', methods=['GET'])
def get_urlmap(short_link):
    """Получение оригинальной ссылки по указанному короткому идентификатору."""
    urlmap = URLMap.query.filter_by(short=short_link).first()
    validate_api_get_url(urlmap)
    return jsonify({'urlmap': urlmap.to_dict()}), 200


@app.route('/api/id/',  methods=['POST'])
def add_urlmap():
    """Cоздание новой короткой ссылки."""
    data = request.get_json()

    validate_api_body(data)
    validate_api_data_url(data)
    validate_api_short_link(data)

    new_link = URLMap()
    new_link.from_dict(data)
    db.session.add(new_link)
    db.session.commit()
    return jsonify({'new_link': new_link.to_dict()}), 201
