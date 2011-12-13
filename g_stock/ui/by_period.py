#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from datetime import date
from PyQt4 import QtGui
from PyQt4 import QtCore

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, \
                            F_PageTitle, FormLabel


class by_periodViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):
        super(by_periodViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)

        self.table = by_periodTableWidget(parent=self)
        self.title = F_PageTitle(u"Les rapports dans le magasin: ")
        self.on_date = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.end_date = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.button = QtGui.QPushButton(_(u"ok"))
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
        vbox.addWidget(self.title)
        vbox.addLayout(gridbox)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def rapport_filter(self):
        on_date = self.on_date.text()
        end_date = self.end_date.text()
        by_periodTableWidget(self, on_date, end_date)


class by_periodTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, on_date=None, end_date=None, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), _(u"Produit"), \
                       _(u"Nombre de carton"), _(u"Carto Restant"), \
                       _(u"Date")]
        if on_date or end_date:
            self.on_date = self.format_date(on_date)
            self.end_date = self.format_date(end_date)
        else:
            self.on_date = "2011-01-01"
            self.end_date = date.today().strftime("%Y-%M-%d")
        self.set_data_for()
        self.refresh(True)

    def refresh_period(self):
        self.set_data_for()
        self.refresh()

    def format_date(self, valeur):
        print valeur
        valeur = str(valeur)
        day, month, year = valeur.split('/')
        return '-'.join(["20" + year, month, day])

    def set_data_for(self):
        print self.on_date, self.end_date
        self.data = [(rap.type_, rap.produit, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                            .filter(Rapport.date_rapp.__gt__(self.on_date)) \
                            .filter(Rapport.date_rapp.__lt__(self.end_date))]
        print self.data
