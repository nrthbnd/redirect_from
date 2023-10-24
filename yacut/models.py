from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель для коротких ссылок и их длинных оригиналов."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(512), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Вернуть оригинальную ссылку из модели в словаре."""
        return dict(
            url=self.original,
            short_link=self.short
        )

    def from_dict(self, data):
        """Записать полученные данные в модель."""
        if 'url' in data:
            setattr(self, 'original', data['url'])
        if 'custom_id' not in data:
            from .views import get_unique_short_id
            new_link = get_unique_short_id()
            setattr(self, 'short', new_link)
        else:
            setattr(self, 'short', data['custom_id'])
