#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from datetime import date, timedelta
from PyQt4 import QtGui
from PyQt4 import QtCore

from database import *
from common import (F_Widget, F_TableWidget, F_PageTitle,
                    FormLabel,  Button, FormatDate)
from data_helper import format_date


class By_periodViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(By_periodViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)

        self.table = By_periodTableWidget(parent=self)
        self.title = F_PageTitle(_(u"Periodic report"))

        self.on_date = FormatDate(QtCore.QDate(date.today().year, 01, 01))
        self.end_date = FormatDate(QtCore.QDate.currentDate())
        self.Button = Button(_(u"OK"))
        self.Button.clicked.connect(self.rapport_filter)
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

        #~ gridbox.addWidget(FormLabel(_("Reports of ") + \
                                    #~ self.on_date.text() + _(u" to ") + \
                                    #~ self.end_date.text()), 4, 3)
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


class By_periodTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), _(u"Store"), _(u"Product"), \
                       _(u"Number of carton"), _(u"Remaining"), \
                       _(u"Date")]

        self.set_data_for()
        self.refresh(True)

    def refresh_period(self, l_date):
        self._reset()
        self.set_data_for(l_date)
        self.refresh()

    def set_data_for(self, *args):
        if args:
            self.data = [(rap.type_, rap.magasin, rap.produit, rap.nbr_carton,
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                            .filter(Rapport.date_rapp.__ge__(args[0][0])) \
                            .filter(Rapport.date_rapp.__le__(args[0][1]))]


    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _("input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"),
                                                      u"")
        if column == 0 and self.data[row][0] == _("inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"),
                                                      u"")
        return super(By_periodTableWidget, self)._item_for_data(row, column,
                                                              data, context)
