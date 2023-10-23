from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель для коротких ссылок и их длинных оригиналов."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(512), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Метод для возвращения в словаре из модели оригинальной ссылки
    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short
        )

    # Метод-десериализатор для записи полученных данных в модель
    def from_dict(self, data):
        if 'url' in data:
            setattr(self, 'original', data['url'])
        if 'custom_id' not in data:
            from .views import get_unique_short_id
            new_link = get_unique_short_id()
            setattr(self, 'short', new_link)
        else:
            setattr(self, 'short', data['custom_id'])
