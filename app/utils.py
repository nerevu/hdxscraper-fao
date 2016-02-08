#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

"""
utils
~~~~~

Provides miscellaneous utility methods
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import requests
import itertools as it

from StringIO import StringIO
from zipfile import ZipFile
from tabutils import io, process as pr, fntools as ft


def get_file(location, **kwargs):
    """Fetches csv from zipped data file"""
    url = '%s/%s' % (kwargs['BASE_URL'], location)
    r = requests.get(url)
    zipfile = ZipFile(StringIO(r.content))
    filename = zipfile.namelist()[0]

    # wrap in StringIO to access `seek`
    f = StringIO(zipfile.open(filename, mode='rU').read())
    return f, 'csv', r.encoding


def normalize(records, **kwargs):
    first = records.next()
    reconstituted = it.chain([first], records)
    filterfunc = lambda x: x[0].startswith('y')
    base = dict(it.ifilterfalse(filterfunc, first.items()))

    for record in reconstituted:
        values = it.ifilter(filterfunc, record.items())

        for addon in ({'year': v[0][1:], 'value': v[1]} for v in values):
            if not ft.is_null(addon['value'], blanks_as_nulls=True):
                yield pr.merge([base, addon])


def gen_data(location=None, **kwargs):
    """Generates records from csv"""
    f, ext, encoding = get_file(location, **kwargs)
    records = io.read_csv(f, sanitize=True, encoding=encoding)
    return normalize(records)


def gen_data_alt(**kwargs):
    base = kwargs('BASE_URL_ALT')

    # Get all dbs
    r = requests.get('%s/databases.json' % base)
    items = r.json()['result']['list']['items']
    dbs = {i['urn'].replace('faodata:database:', ''): i['uri'] for i in items}
    db = dbs[kwargs['db_name']]
    # db = 'gmfs-geonetwork'

    # Get all datasets
    url = '%s/%s/datasets.json' % (base, db)
    params = {'fields': 'mnemonic, label@en'}
    r = requests.get(url, params=params)
    items = r.json()['result']['list']['items']
    datasets = {i['?']: i['mnemonic'] for i in items}
    dataset = datasets[kwargs['ds_name']]
    # dataset = 'places'

    # Get all fields
    url = '%s/%s/%s/measures.json' % (base, db, dataset)
    params = {'fields': 'mnemonic, label@en, unitMeasure'}
    r = requests.get(url, params=params)
    items = r.json()['result']['list']['items']
    fields = [i['?'] for i in items]

    # Get all data
    url = '%s/%s/%s/facts.json' % (base, db, dataset)

    params = {
        # 'fields': 'year, cnt.iso3 as Country, item.label, m5111 as Stocks',
        'fields': ','.join(fields),
        'filter': 'year eq 2010',
        # 'filter': 'cnt.iso3 eq AFG',
        'page': 1,
        'pageSize': 50,
    }

    r = requests.get(url, params=params)
    return iter(r.json()['result']['list']['items'])
