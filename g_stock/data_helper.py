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
    """ """
    list_alert = []
    for mag in session.query(Magasin):
        for prod in session.query(Produit):
            f = last_rapport(mag.id, prod.id)
            if f:
                if f.restant <= 100:
                    list_alert.append(f)
    return list_alert


def remaining(type_, nbr_carton, magasin, produit):
    """ Calculation of remaining. """
    previous_rapp = ""
    previous_rapp = last_rapport(magasin, produit)
    if type_ == _(u"inout"):
        try:
            restant = int(previous_rapp.restant) - int(nbr_carton)
            if restant < 0:
                return [None, _(u"You can not do this because") + \
                                    str(previous_rapp.restant) + " < " \
                                    + str(nbr_carton)]
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


def inventaire(on_date, end_date):
    """ """
    list_rap = []
    reports = session.query(Rapport)\
                    .filter(Rapport.date_rapp.__ge__(on_date)) \
                    .filter(Rapport.date_rapp.__le__(end_date))
    for mag in session.query(Magasin).all():
        for prod in session.query(Produit).all():
            p =reports.filter(Rapport.magasin_id == mag.id) \
                        .filter(Rapport.produit_id == prod.id)\
                        .order_by("-date_rapp")
            try:
                list_rap.append(p[0])
            except:
                pass
    return list_rap
