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
        super(InventaireViewWidget, self).__init__(parent=parent, *args,
                                                                **kwargs)

        self.table = InventaireTableWidget(parent=self)
        self.title = F_PageTitle(_(u"Inventory"))

        self.on_date = FormatDate(QtCore.QDate(date.today().year,\
                                                            01, 01))
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
        l_date = [format_date(self.on_date.text()),
                  format_date(self.end_date.text())]
        self.table.refresh_period(l_date)

    def rapport_filter(self):
        self.refresh()


class InventaireTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Store"), _(u"Product"), _(u"Quantity"),
                                    _(u"Price U."), _(u"Montant")]
        self.set_data_for()
        self.refresh(True)

    def extend_rows(self):
        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 1)
        self.setSpan(nb_rows, 0, 1, 3)
        self.button = Button_export(_("Exporter"))
        self.button.released.connect(self.export_data)
        self.setCellWidget(nb_rows, 3, self.button)


    def _item_for_data(self, row, column, data, context=None):
        if column == 3:
            line_edit = QtGui.QLineEdit(u"%d" % 0)
            line_edit.setValidator(QtGui.QIntValidator())
            line_edit.editingFinished.connect(self.changed_value)
            return line_edit
        return super(InventaireTableWidget, self)\
                                    ._item_for_data(row, column, data,
                                                    context)

    def changed_value(self, refresh=False):

        print "changed_value"
        # change self.data to reflect new budgets
        for row_num in xrange(0, self.data.__len__()):
            self._update_budget(row_num, int(self.item(row_num, 2).text()),
                                int(self.cellWidget(row_num, 3).text()))
        # we don't refresh table unless asked
        # so that we can forward click events
        if refresh:
            self.refresh()
        # focus on save button
        #~ self.button.setFocus(Qt.MouseFocusReason)

    def _update_budget(self, row_num, qte, price):
        d = self.data[row_num]
        print "d", d[2], d[3], d[4], qte, price
        #~ self.data[row_num] = (d[0], d[1], d[2], budget, d[4])

    def export_data():
        print "export ok"

    def refresh_period(self, l_date):
        self._reset()
        self.set_data_for(l_date)
        self.refresh()

    def set_data_for(self, *args):

        if args:
            reports = last_mouvement_report(args[0][0], args[0][1])
            self.data = [(rap.magasin, rap.produit, rap.restant,"", "")
                          for rap in reports]
