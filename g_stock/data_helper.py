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
    last_rapp = session.query(Rapport).filter(Rapport.magasin_id == magasin)\
                                      .filter(Rapport.produit_id == produit)\
                                      .order_by(desc(Rapport.date_rapp))\
                                      .first()
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
                        u" Car " + str(previous_rapp.restant) + " < " \
                                + str(nbr_carton)]
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

