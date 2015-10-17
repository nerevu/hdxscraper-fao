from os import path as p

# module vars
_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_db_name = 'scraperwiki.sqlite'
_project = 'hdxscraper-fao'


# configuration
class Config(object):

    BASE_URL = 'http://faostat3.fao.org/faostat-bulkdownloads'
    TABLES = {
        'Shipments': 'Food_Aid_Shipments_WFP_E_All_Data.zip',
        'Security': 'Food_Security_Data_E_All_Data.zip',
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_basedir, _db_name)
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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % p.join(_parentdir, _db_name)


class Production(Config):
    PROD = True


class Development(Config):
    DEBUG = True
    API_LIMIT = 50
    ROW_LIMIT = 50


class Test(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    API_LIMIT = 10
    ROW_LIMIT = 10
    TESTING = True
