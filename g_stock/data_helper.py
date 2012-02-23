#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from datetime import date, timedelta

from sqlalchemy import desc, asc

from database import *


def last_rapport(magasin_id, produit_id):
    """ last Rapport
    prams: magasin_id et produit_id"""
    return session.query(Rapport)\
                                .filter(Rapport.magasin_id == magasin_id)\
                                .filter(Rapport.produit_id == produit_id)\
                                .order_by(desc(Rapport.date_rapp)).first()


def alerte_report():
    """ Return la liste des produits inferieur à 30 0"""

    list_alert = [last_rapport(mag.id, prod.id)
                  for prod in session.query(Produit)
                  for mag in session.query(Magasin)
                  if last_rapport(mag.id, prod.id) != None
                  and last_rapport(mag.id, prod.id).restant <= 30]
    return list_alert


def remaining(type_, nbr_carton, magasin, produit):
    """ Calculation of remaining. """

    previous_rapp = ""
    previous_rapp = last_rapport(magasin, produit)
    if type_ == _(u"inout"):
        try:
            restant = int(previous_rapp.restant) - int(nbr_carton)
            if restant < 0:
                return [None, _(u"You can not do this because") +
                        str(previous_rapp.restant) + " < " + str(nbr_carton)]
            return [restant, u""]
        except AttributeError:
            return [None, _(u"There were no entry for this product ")]
    if type_ == _(u"input"):
        try:
            restant = int(previous_rapp.restant) + int(nbr_carton)
            return [restant, u""]
        except AttributeError:
            return [int(nbr_carton), u""]


def update_rapport(report):
    """ mise à jour après la suppression"""
    rapports = session.query(Rapport) \
                .filter(Rapport.magasin_id == report.magasin_id) \
                .filter(Rapport.produit_id == report.produit_id)
    prev_report = []
    prev_report = rapports\
                  .filter(Rapport.date_rapp.__lt__(report.date_rapp)) \
                  .order_by(desc(Rapport.date_rapp)).first()
    if prev_report:
        rest = prev_report.restant
        next_report = [(rap) for rap in session.query(Rapport) \
                .filter(Rapport.magasin_id == prev_report.magasin_id) \
                .filter(Rapport.produit_id == prev_report.produit_id) \
                .filter(Rapport.date_rapp.__gt__(prev_report.date_rapp)) \
                .order_by(asc(Rapport.date_rapp)).all()]
    else:
        next_report = rapports \
                      .filter(Rapport.date_rapp.__gt__(report.date_rapp)) \
                      .order_by(asc(Rapport.date_rapp)).all()
        rest = 0
    if next_report != []:
        for rap in next_report:
            rap.restant = rest
            if rap.type_ == _(u"input"):
                rap.restant = rest + rap.nbr_carton
            if rap.type_ == _(u"inout"):
                rap.restant = rest - rap.nbr_carton
            rest = rap.restant
            session.add(rap)
            session.commit()


def last_mouvement_report(*args, **kargs):
    """
    prams: on_date, end_date, Magasin, Produit"""
    try:
        on_date = args[0]
        end_date = args[1]
    except IndexError:
        on_date = end_date = None

    reports = report_periodic(on_date, end_date)

    product = session.query(Produit).order_by('libelle').all()
    store = session.query(Magasin).order_by('name').all()

    if "product" in kargs.keys():
        product = [kargs["product"]]

    if "store" in kargs.keys():
        store = [kargs["store"]]

    list_rap = []
    for mag in store:
        for prod in product:
            p = reports.filter(Rapport.magasin == mag) \
                       .filter(Rapport.produit == prod)\
                       .order_by(desc(Rapport.date_rapp))
            try:
                list_rap.append(p[0])
            except IndexError:
                pass
    return list_rap


def report_periodic(on_date=None, end_date=None):
    """ """
    reports = session.query(Rapport)
    if on_date != None:
        reports = reports.filter(Rapport.date_rapp.__ge__(on_date)) \
                         .filter(Rapport.date_rapp.__le__(end_date))
    return reports


def format_date(dat):
    dat = str(dat)
    day, month, year = dat.split('/')
    return '-'.join([year, month, day])
