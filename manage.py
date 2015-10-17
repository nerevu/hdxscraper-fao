#!/usr/bin/env python
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import os.path as p

from subprocess import call

from pprint import pprint
from flask import current_app as app
from flask.ext.script import Manager
from tabutils.fntools import chunk

from app import create_app, db, utils, models

manager = Manager(create_app)
manager.add_option('-m', '--mode', default='Development')
manager.main = manager.run

_basedir = p.dirname(__file__)


@manager.command
def check():
    """Check staged changes for lint errors"""
    call(p.join(_basedir, 'bin', 'check-stage'), shell=True)


@manager.command
def lint():
    """Check style with flake8"""
    call('flake8')


@manager.command
def pipme():
    """Install requirements.txt"""
    call('sudo pip install -r requirements.txt', shell=True)


@manager.command
def require():
    """Create requirements.txt"""
    cmd = 'pip freeze -l | grep -vxFf dev-requirements.txt > requirements.txt'
    call(cmd, shell=True)


@manager.command
def test():
    """Run nose and script tests"""
    call('nosetests -xv', shell=True)


@manager.command
def createdb():
    """Creates database if it doesn't already exist"""

    with app.app_context():
        db.create_all()
        print('Database created')


@manager.command
def cleardb():
    """Removes all content from database"""

    with app.app_context():
        db.drop_all()
        print('Database cleared')


@manager.command
def setup():
    """Removes all content from database and creates new tables"""

    with app.app_context():
        cleardb()
        createdb()


def populate():
    """Populates db with most recent data"""
    limit = 0

    with app.app_context():
        for table_name, location in app.config['TABLES'].items():
            table = getattr(models, table_name)
            row_limit = app.config['ROW_LIMIT']
            chunk_size = min(row_limit or 'inf', app.config['CHUNK_SIZE'])
            debug, test = app.config['DEBUG'], app.config['TESTING']

            if test:
                createdb()

            data = utils.gen_data(app.config, location)

            del_count = table.query.delete(synchronize_session=False)
            db.session.commit()

            if debug:
                print(
                    'Deleted %s records from the %s table...' % (
                        del_count, table_name))

            for records in chunk(data, chunk_size):
                in_count = len(records)
                limit += in_count

                if debug:
                    print(
                        'Inserting %s records into the %s table...' % (
                            in_count, table_name))

                if test:
                    pprint(records)

                db.engine.execute(table.__table__.insert(), records)

                if row_limit and limit >= row_limit:
                    break

            if debug:
                print(
                    'Successfully inserted %s records into the %s table!' % (
                        limit, table_name))


@manager.command
def run():
    """Populates all tables in db with most recent data"""
    with app.app_context():
        sw = app.config['SW']
        utils.run_or_schedule(populate, sw, utils.exception_handler)


if __name__ == '__main__':
    manager.run()
