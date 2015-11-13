# -*- coding: utf-8 -*-
"""
    app.models
    ~~~~~~~~~~

    Provides the SQLAlchemy models
"""
from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import savalidation.validators as val

from app import db
from savalidation import ValidationMixin


class Shipments(db.Model, ValidationMixin):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)

    # other keys
    item = db.Column(db.String(128), nullable=False)
    item_code = db.Column(db.String(8), nullable=False)
    donor_country = db.Column(db.String(64), nullable=False)
    donor_country_code = db.Column(db.String(8), nullable=False)
    recipient_country = db.Column(db.String(64), nullable=False)
    recipient_country_code = db.Column(db.String(8), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    year = db.Column(db.String(16), nullable=False)
    value = db.Column(db.String(32), nullable=False)

    # validation
    val.validates_constraints()

    def __repr__(self):
        return ('<Shipments(%r, %r)>' % (self.item, self.year))


class Security(db.Model, ValidationMixin):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)

    # other keys
    item = db.Column(db.String(128), nullable=False)
    item_code = db.Column(db.String(8), nullable=False)
    element = db.Column(db.String(16), nullable=False)
    element_code = db.Column(db.String(8), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    country_code = db.Column(db.String(8), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    year = db.Column(db.String(16), nullable=False)
    value = db.Column(db.String(32), nullable=False)

    # validation
    val.validates_constraints()

    def __repr__(self):
        return ('<Security(%r, %r)>' % (self.item, self.year))


class Prices(db.Model, ValidationMixin):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)

    # other keys
    item = db.Column(db.String(128), nullable=False)
    item_code = db.Column(db.String(8), nullable=False)
    element = db.Column(db.String(16), nullable=False)
    element_code = db.Column(db.String(8), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    country_code = db.Column(db.String(8), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    year = db.Column(db.String(16), nullable=False)
    value = db.Column(db.String(32), nullable=False)

    # validation
    val.validates_constraints()

    def __repr__(self):
        return ('<Prices(%r, %r)>' % (self.item, self.year))


class Indices(db.Model, ValidationMixin):
    # auto keys
    id = db.Column(db.Integer, primary_key=True)

    # other keys
    item = db.Column(db.String(128), nullable=False)
    item_code = db.Column(db.String(8), nullable=False)
    element = db.Column(db.String(16), nullable=False)
    element_code = db.Column(db.String(8), nullable=False)
    country = db.Column(db.String(64), nullable=False)
    country_code = db.Column(db.String(8), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    year = db.Column(db.String(16), nullable=False)
    value = db.Column(db.String(32), nullable=False)

    # validation
    val.validates_constraints()

    def __repr__(self):
        return ('<Indices(%r, %r)>' % (self.item, self.year))
