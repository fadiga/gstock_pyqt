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


class Date_pagination():
    """
    navigation entre les dates année, mois, week """

    def __init__(self, year, duration, duration_number):

        self.year = year
        self.duration = duration
        self.duration_number = duration_number

        todays_date_is_before = False
        todays_date_is_after = False

        # la date du jour
        todays_date = date.today()

        if duration == "week":
            # on recupere le premier jour
            current_date = get_week_boundaries(year, duration_number)[0]

            # la date de la semaine avant celle qu'on affiche
            delta = timedelta(7)
            previous_date = current_date - delta
            previous_week_number = previous_date.isocalendar()[1]

            # la date de la semaine après celle qu'on affiche
            next_date = current_date + delta
            next_week_number = next_date.isocalendar()[1]

            # la date de la semaine avant celle qu'on affiche
            two_dates_ago = current_date - (delta * 2)

            # la date de la semaine avant celle qu'on affiche
            in_two_dates = current_date + (delta * 2)

            # Vérification que la semaine d'aujourd'hui est à afficher ou non
            if todays_date <= two_dates_ago:
                todays_date_is_before = True

            if todays_date >= in_two_dates:
                todays_date_is_after = True

            # formatage de l'affichage des mois
            current_date_ = current_date
            previous_date_ = previous_date
            next_date_ = next_date
            todays_date = u"Cette semaine"

        elif duration == "month":

            current_date = date(year, duration_number, 1)

             # la date du mois avant celui qu'on affiche
            delta = timedelta(1)
            previous_date = current_date - delta
            previous_date = date(previous_date.year, previous_date.month, 1)

            # la date du mois après celui qu'on affiche
            days_count = monthrange(current_date.year, current_date.month)[1]
            delta = timedelta(days_count + 1)
            next_date = current_date + delta

            # Vérification que la semaine d'aujourd'hui est à afficher ou non
            if todays_date < previous_date:
                todays_date_is_before = True

            if todays_date > next_date:
                todays_date_is_after = True

            # formatage de l'affichage des mois en tenant compte de la
            #language code
            current_date_ = current_date
            previous_date_ = previous_date
            next_date_ = next_date
            todays_date = u"Ce mois ci"

        else:

            current_date = date(year, 1, 1)

             # la date de l'année avant celle qu'on affiche
            previous_date = date(current_date.year - 1,
                                 current_date.month,
                                 current_date.day)

            # la date de l'année après celle qu'on affiche
            next_date = date(current_date.year + 1,
                                 current_date.month,
                                 current_date.day)

            # Vérification que l'année d'aujourd'hui est à afficher ou non
            if todays_date.year < (current_date.year - 1):
                todays_date_is_before = True

            if todays_date.year > (current_date.year + 1):
                todays_date_is_after = True

            # formatage de l'affichage des années
            current_date_ = current_date.strftime("%Y")
            previous_date_ = previous_date.strftime("%Y")
            next_date_ = next_date.strftime("%Y")
            todays_date = u"Cette année"

    def display_name(self):
        return (u"%(quar)s") % {'quar': self.current_date_}

    def current_date(self):
        return (u"%(quarter)s") % {'quarter': current_date_}

    def next(self):
        return self.next_date_

    def previous(self):
        return  self.previous_date_

    def __unicode__(self):
        return self.current_date_

    def get_week_boundaries(year, week):
        """
            Retoure les date du premier et du dernier jour de la semaine dont
            on a le numéro.
        """
        d = date(year, 1, 1)
        if(d.weekday() > 3):
            d = d + timedelta(7 - d.weekday())
        else:
            d = d - timedelta(d.weekday())

        dlt = timedelta(days=(week - 1) * 7)
        return d + dlt, d + dlt + timedelta(days=6)


def get_duration_pagination(year, duration, duration_number):
    """
    navigation entre les dates: année, mois, week """
    # la date d'aujourd'hui
    week_date_url, month_date_url, year_date_url = "", "", ""

    if duration == "week":
        # l'adresse pour afficher le mois
        month = get_week_boundaries(year, duration_number)[0].month

        month_date_url = (year, "month", month)

        # l'adresse pour afficher l'année
        year_date_url = year

    elif duration == "month":

        year, week, day = date(year, duration_number, 1).isocalendar()

        # l'adresse pour afficher la semaine
        week_date_url = (year, "week", week)

        # l'adresse pour afficher l'année
        year_date_url = (year)

    else:
        # l'adresse pour afficher la semaine
        week_numbers = date.today().isocalendar()
        week_date_url = (year, "week", week_numbers[1])
        # l'adresse pour afficher le mois
        month_date_url = (year, "month", date.today().month)
    return (week_date_url, month_date_url, year_date_url)
