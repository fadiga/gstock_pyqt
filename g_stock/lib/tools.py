#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad

from datetime import date, timedelta
from calendar import monthrange


class Date_pagination():
    """
    navigation entre les dates année, mois, week """

    def __init__(self, year=date.today().year, duration="week", duration_number= 46):

        self.year = year
        self.duration = duration
        self.duration_number = duration_number

        todays_date_is_before = False
        todays_date_is_after = False

        # la date du jour
        todays_date = date.today()

        if duration == "week":
            # on recupere le premier jour
            current_date = self.get_week_boundaries(self.year, \
                                                    self.duration_number)[0]

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
            self.current_date_ = current_date
            self.previous_date_ = previous_date
            self.next_date_ = next_date
            self.todays_date = u"Cette semaine"

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
            self.current_date_ = current_date
            self.previous_date_ = previous_date
            self.next_date_ = next_date
            self.todays_date = u"Ce mois ci"

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
            self.current_date_ = current_date.strftime("%Y")
            self.previous_date_ = previous_date.strftime("%Y")
            self.next_date_ = next_date.strftime("%Y")
            self.todays_date = u"Cette année"
    @property
    def display_name(self):
        return self.current_date_.strftime("%X")
    @property
    def current_date(self):
        return self.current_date_
    @property
    def next_date(self):
        return self.next_date_
    @property
    def previous(self):
        return self.previous_date_
    @property
    def todays_date(self):
        return  self.todays_date

    def __repr__(self):
        return (u"%(prev)s %(current)s %(next)s") % {"prev": self.previous, \
                "current": self.current_date, "next": self.next_date}

    def __unicode__(self):
        return (u"%(prev)s %(current)s %(next)s") % {"prev": self.previous, \
                "current": self.current_date, "next": self.next_date}

    def get_week_boundaries(self, year, week):
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
