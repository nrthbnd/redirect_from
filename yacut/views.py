import random
import string
from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request
from markupsafe import Markup

from settings import LENGTH_OF_NEW_LINK

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    """Сгенерировать короткую ссылку."""
    short_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=LENGTH_OF_NEW_LINK))
    if URLMap.query.filter_by(short=short_string).first() is None:
        return short_string
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Отобразить главную страницу."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if not form.custom_id.data:
        short_string = get_unique_short_id()
        form.custom_id.data = short_string
    if URLMap.query.filter_by(short=form.custom_id.data).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    new_link = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data
    )
    db.session.add(new_link)
    db.session.commit()
    new_url = request.base_url + form.custom_id.data
    flash(Markup(f'Ваша ссылка: <a href="{new_url}">{new_url}</a>'))
    return render_template('index.html', form=form)


@app.route('/<string:short_string>')
def redirect_view(short_string):
    """Переадресовать с короткой ссылки на оригинальную."""
    return redirect(
        URLMap.query.filter_by(short=short_string).first_or_404().original
    )
