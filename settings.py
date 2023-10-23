import os

"""Длина ссылки по умолчанию."""
LENGTH_OF_NEW_LINK = 6
LOCAL_HOST = 'http://localhost/'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
