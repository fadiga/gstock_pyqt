#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from datetime import date, timedelta
from PyQt4 import QtGui
from PyQt4 import QtCore

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, \
                                                F_PageTitle, FormLabel


class By_periodViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):
        super(By_periodViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)

        list_date = parent.list_
        self.table = By_periodTableWidget(list_date, parent=self)
        self.title = F_PageTitle(u"Rapport periodique ")

        if list_date:
            on, end = list_date
        self.on_date = QtGui.QDateEdit(QtCore.QDate(date.today().year,01,01))
        self.on_date.setDisplayFormat("dd/MM/yyyy")
        self.on_date.setCalendarPopup(True)
        self.end_date = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date.setCalendarPopup(True)
        self.button = QtGui.QCommandLinkButton(_(u"ok"))
        self.button.clicked.connect(self.rapport_filter)
        vbox = QtGui.QVBoxLayout()
        # Grid
        gridbox = QtGui.QGridLayout()
        gridbox.addWidget(FormLabel(u"Date debut"), 0, 1)
        gridbox.addWidget(self.on_date, 0, 2)
        gridbox.addWidget(FormLabel(u"Date fin"), 1, 1)
        gridbox.addWidget(self.end_date, 1, 2)
        gridbox.addWidget(FormLabel(""), 0, 3)
        gridbox.addWidget(self.button, 2, 2)
        gridbox.setColumnStretch(3, 5)
        if list_date:
            gridbox.addWidget(FormLabel("Les Rapports du" + on + " au " + \
                                                                end ), 4, 3)
        else:
            gridbox.addWidget(FormLabel("Les Rapports du " + \
                                        self.on_date.text() + " au " + \
                                        self.end_date.text()), 4, 3)
        vbox.addWidget(self.title)
        vbox.addLayout(gridbox)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def rapport_filter(self):
        on_date = self.on_date.text()
        end_date = self.end_date.text()
        l_date = [on_date, end_date]
        self.change_main_context(By_periodViewWidget, l_date)


class By_periodTableWidget(F_TableWidget):
    """ """

    def __init__(self, list_date, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [u"Type", u"Magasin", u"Produit", u"Nombre de carton", \
                                                    u"Carto Restant", u"Date"]
        try:
            self.on_date = self.format_date(list_date[0])
            self.end_date = self.format_date(list_date[1])
        except:
            self.on_date = (date.today() - timedelta(365)).strftime("%Y-%m-%d")
            self.end_date = date.today().strftime("%Y-%m-%d")
        self.set_data_for()
        self.refresh(True)

    def refresh_period(self):
        self.set_data_for()
        self.refresh()

    def format_date(self, valeur):
        valeur = str(valeur)
        day, month, year = valeur.split('/')
        return '-'.join([year, month, day])

    def set_data_for(self):
        self.data = [(rap.type_, rap.magasin, rap.produit, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                            .filter(Rapport.date_rapp.__ge__(self.on_date)) \
                            .filter(Rapport.date_rapp.__le__(self.end_date))]
