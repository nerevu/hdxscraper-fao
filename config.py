# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
config
~~~~~~

Provides app configuration settings
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from os import path as p

BASEDIR = p.dirname(__file__)
PARENTDIR = p.dirname(BASEDIR)
DB_NAME = 'scraperwiki.sqlite'
RECIPIENT = 'reubano@gmail.com'


class Config(object):
    suffix = '_E_All_Data.zip'
    BASE_URL = 'http://faostat3.fao.org/faostat-bulkdownloads'
    BASE_URL_ALT = 'http://data.fao.org/developers/api/v1/en/resources'
    TABLES = [
        {'name': 'shipments', 'location': 'Food_Aid_Shipments_WFP%s' % suffix},
        {'name': 'security', 'location': 'Food_Security_Data%s' % suffix},
        {'name': 'prices', 'location': 'Prices%s' % suffix},
        {'name': 'indices', 'location': 'Price_Indices%s' % suffix},
    ]

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(BASEDIR, DB_NAME)
    LOGFILE = p.join(BASEDIR, 'http', 'log.txt')
    API_LIMIT = 1000
    SW = False
    DEBUG = False
    TESTING = False
    PROD = False
    CHUNK_SIZE = 2 ** 14
    ROW_LIMIT = None


class Scraper(Config):
    PROD = True
    SW = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(PARENTDIR, DB_NAME)
    LOGFILE = p.join(PARENTDIR, 'http', 'log.txt')


class Production(Config):
    PROD = True


class Development(Config):
    DEBUG = True
    CHUNK_SIZE = 2 ** 4
    ROW_LIMIT = 50


class Test(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    CHUNK_SIZE = 2 ** 4
    ROW_LIMIT = 10
    TESTING = True
