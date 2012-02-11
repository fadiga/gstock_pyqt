#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from datetime import date, timedelta

from PyQt4 import QtGui
from PyQt4 import QtCore

from database import *
from common import (F_Widget, F_TableWidget, F_PageTitle,
                    FormLabel, Button_export, Button, FormatDate)
from data_helper import last_mouvement_report, format_date


class InventaireViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(InventaireViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)

        self.table = InventaireTableWidget(parent=self)
        self.title = F_PageTitle(_(u"Inventory"))

        self.on_date = FormatDate(QtCore.QDate(date.today().year,01,01))
        self.end_date = FormatDate(QtCore.QDate.currentDate())
        self.Button = Button(u"Ok")
        self.Button.clicked.connect(self.rapport_filter)
        self.Button_export = Button_export(_(u"Export xls"))
        self.Button_export.clicked.connect(self.rapport_filter)
        vbox = QtGui.QVBoxLayout()
        # Grid
        gridbox = QtGui.QGridLayout()
        gridbox.addWidget(FormLabel(_(u"On date")), 0, 1)
        gridbox.addWidget(self.on_date, 0, 2)
        gridbox.addWidget(FormLabel(_(u"End date")), 1, 1)
        gridbox.addWidget(self.end_date, 1, 2)
        gridbox.addWidget(FormLabel(""), 0, 3)
        gridbox.addWidget(self.Button, 2, 2)
        gridbox.setColumnStretch(3, 5)
        gridbox.addWidget(self.Button_export, 2, 6)
        vbox.addWidget(self.title)
        vbox.addLayout(gridbox)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def refresh(self):
        l_date = [format_date(self.on_date.text()), \
                  format_date(self.end_date.text())]
        self.table.refresh_period(l_date)

    def rapport_filter(self):
        self.refresh()


class InventaireTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), _(u"Store"), _(u"Product"), \
                       _(u"Number of carton "), _(u"Remaining"), \
                       _(u"Date")]

        self.set_data_for()
        self.refresh(True)

    def extend_rows(self):

        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 1)
        self.setSpan(nb_rows, 0, 1, 3)
        self.button = Button_export(_("Exporter"))
        self.button.released.connect(self.export_data)
        self.setCellWidget(nb_rows, 3, self.button)

    def export_data():
        print "export ok"
        
    def refresh_period(self, l_date):
        self._reset()
        self.set_data_for(l_date)
        self.refresh()

    def set_data_for(self, *args):
        
        if args:
            reports = last_mouvement_report(args[0][0], args[0][1])
            self.data = [(rap.type_, rap.magasin, rap.produit, rap.nbr_carton,
                          rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                          for rap in reports]
