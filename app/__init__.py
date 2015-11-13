# -*- coding: utf-8 -*-
"""
    app
    ~~~

    Provides the flask application
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import config

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = '0.10.2'

__title__ = 'hdxscraper-fao'
__author__ = 'Reuben Cummings'
__description__ = (
    'Collector for UN Food and Agriculture Organization (FAO) Humanitarian'
    'Data')

__email__ = 'reubano@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Reuben Cummings'

db = SQLAlchemy()


def create_app(mode=None):
    app = Flask(__name__)
    db.init_app(app)

    if mode:
        app.config.from_object(getattr(config, mode))
    else:
        app.config.from_envvar('APP_SETTINGS', silent=True)

    return app
