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

import time
import schedule as sch
import smtplib
import logging
import scraperwiki
import requests
import itertools as it

from os import environ, path as p
from email.mime.text import MIMEText
from StringIO import StringIO
from zipfile import ZipFile

from config import _project
from tabutils import io, process as pr, fntools as ft

_basedir = p.dirname(__file__)
_parentdir = p.dirname(_basedir)
_schedule_time = '10:30'
_recipient = 'reubano@gmail.com'

logging.basicConfig()
logger = logging.getLogger(_project)


def send_email(_to, _from=None, subject=None, text=None):
    user = environ.get('user')
    _from = _from or '%s@scraperwiki.com' % user
    subject = subject or 'scraperwiki box %s failed' % user
    text = text or 'https://scraperwiki.com/dataset/%s' % user
    msg = MIMEText(text)
    msg['Subject'], msg['From'], msg['To'] = subject, _from, _to

    # Send the message via our own SMTP server, but don't include the envelope
    # header.
    s = smtplib.SMTP('localhost')
    s.sendmail(_from, [_to], msg.as_string())
    s.quit()


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            scraperwiki.status('error', 'Error collecting data')

            with open(p.join(_parentdir, 'http', 'log.txt'), 'rb') as f:
                send_email(_recipient, text=f.read())
        else:
            scraperwiki.status('ok')

    return wrapper


def run_or_schedule(job, schedule=False, exception_handler=None):
    job()

    if schedule:
        job = exception_handler(job) if exception_handler else job
        sch.every(1).day.at(_schedule_time).do(job)

        while True:
            sch.run_pending()
            time.sleep(1)


def gen_data(config, location):
    """Fetches zipped data and generates records"""
    base_url = config['BASE_URL']

    url = '%s/%s' % (base_url, location)
    r = requests.get(url)
    zipfile = ZipFile(StringIO(r.content))

    # wrap in StringIO to access `seek`
    f = StringIO(zipfile.open(zipfile.namelist()[0], mode='rU').read())
    records = list(io.read_csv(f, sanitize=True, encoding=r.encoding))
    filterfunc = lambda x: x[0].startswith('y')
    base = dict(it.ifilterfalse(filterfunc, records[0].items()))

    for record in records:
        values = it.ifilter(filterfunc, record.items())

        for addon in ({'year': v[0][1:], 'value': v[1]} for v in values):
            if not ft.is_null(addon['value'], blanks_as_nulls=True):
                yield pr.merge([base, addon])
