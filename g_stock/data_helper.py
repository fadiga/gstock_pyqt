#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad


import gettext
from datetime import date, datetime

import sqlalchemy
from sqlalchemy import desc, func
from sqlalchemy.orm import exc

from database import *


def last_rapport(magasin, produit):
    """ last Rapport
    prams: magasin_id et produit_id"""
    last_rapp = session.query(Rapport)\
                       .filter(Rapport.magasin_id==magasin)\
                       .filter(Rapport.produit_id==produit)\
                       .order_by(desc(Rapport.date_rapp)).first()
    return last_rapp


def remaining(type_,  nbr_carton, magasin, produit):
    """ Calculation of remaining. """
    previous_rapp = ""
    previous_rapp = last_rapport(magasin, produit)
    if type_ == "Sortie":
        try:
            restant = int(previous_rapp.restant) - int(nbr_carton)
            if restant < 0:
                return [None, u"Vous ne pouvez pas effectie cette operation \n"
                        u" Car " + str(previous_rapp.restant) + " < "+ str(nbr_carton)]
            return [restant, u""]
        except AttributeError:
            return [None, u"IL n'y eu aucun  entre pour ce produit "]
    if type_ == "Entre":
        try:
            restant = int(previous_rapp.restant) + int(nbr_carton)
            return [restant, u""]
        except AttributeError:
            return [int(nbr_carton), u""]


def update_rapport():
    pass

def quarter_for(date_):
    ''' returns quarter a date is part of '''
    if date_ < date(date_.year, 4, 1):
        return 1
    if date_ < date(date_.year, 7, 1):
        return 2
    if date_ < date(date_.year, 10, 1):
        return 3
    return 4


def next_quarter(quarter, year=None):
    ''' return next quarter number '''
    if quarter < 4:
        return (quarter + 1, year)
    return (1, year + 1)


def previous_quarter(quarter, year=None):
    ''' return next quarter number '''
    if quarter > 1:
        return (quarter - 1, year)
    return (4, year - 1)


def quarter_dates(quarter, year):
    ''' returns (start, end) date obj for a quarter and year '''
    if quarter == 1:
        s, e = (1, 1), (3, 31)
    if quarter == 2:
        s, e = (4, 1), (6, 30)
    if quarter == 3:
        s, e = (7, 1), (9, 30)
    if quarter == 4:
        s, e = (10, 1), (12, 31)

    return (date(year, *s), date(year, *e))

def current_period():
    ''' period for today() '''
    return period_for(date.today())


def period_for(date_):
    ''' period object a date is part of '''
    quarter = quarter_for(date_)
    try:
        period = [period for period in \
                  session.query(Rapport)\
                         .filter(func.strftime('%Y', Rapport.date_rapp) \
                                 == date_.strftime('%Y')).all()]
    except IndexError:
        pass
    return period
