#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from PyQt4 import QtCore
from sqlalchemy import desc

from database import *
from util import formatted_number
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle
from by_magasin import By_magasinViewWidget
from by_produit import By_produitViewWidget


class AllreportsViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):

        super(AllreportsViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)
        F_PeriodHolder.__init__(self, *args, **kwargs)

        self.title = F_PageTitle(_(u"All reports"))
        self.table = RapportTableWidget(parent=self, period=self.main_period)
        #Combobox widget
        vbox = QtGui.QVBoxLayout()

        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def change_period_type(self):

        F_PeriodHolder(self, self.main_period)

    def refresh(self):
        self.table.refresh()

    def change_period(self, period):

        self.table.refresh_period(period)


class RapportTableWidget(F_TableWidget):

    def __init__(self, parent, period, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), (u"Magasin No."), _(u"Produit"), \
                       _(u"Nbre carton"), _(u"Restant"), \
                       _(u"Date")]
        self.set_data_for(period)
        self.refresh(True)
        self.setColumnWidth(0, 20)

    def refresh_period(self, period):
        self.main_period = period

        self.set_data_for(period.year)
        self.refresh()

    def set_data_for(self, period):
        self.data = [(rap.type_, rap.magasin, rap.produit, \
                        formatted_number(rap.nbr_carton), \
                        formatted_number(rap.restant), \
                        rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                        .filter(Rapport.date_rapp==period) \
                        .order_by(desc(Rapport.date_rapp)).all()]
        print self.data

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _("input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), u"")
        if column == 0 and self.data[row][0] == _(u"inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), u"")
        return super(RapportTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)

    def click_item(self, row, column, *args):
        magsin_column = 1
        produit_column = 2
        if column == magsin_column:
            self.parent.change_main_context(By_magasinViewWidget, \
                                    magasin=self.data[row][magsin_column])
        if column == produit_column:
            self.parent.change_main_context(By_produitViewWidget, \
                                    produit=self.data[row][produit_column])
        else:
            return
