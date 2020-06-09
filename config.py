# ./config.py
# Using this file and class to store some secrets
# Will add defaults, but this should be changed according to the stage

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # debugging flask on
    DEBUG = True

    # secret key to avoid CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # DB-related configs
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir, 'minibank.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

