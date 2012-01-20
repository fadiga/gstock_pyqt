#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from sqlalchemy import desc

from database import Rapport, session
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
        self.table = RapportTableWidget(parent=self, main_date=self.main_date)
        #Combobox widget
        vbox = QtGui.QVBoxLayout()

        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def change_period(self, main_date):
        self.table.refresh_period(main_date)


class RapportTableWidget(F_TableWidget):

    def __init__(self, parent, main_date, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), (u"Magasin No."), _(u"Produit"), \
                       _(u"Nbre carton"), _(u"Remaining"), _(u"Date")]
        self.set_data_for(main_date)
        self.refresh(True)
        self.setColumnWidth(0, 20)

    def refresh_period(self, main_date):
        """ """
        self.set_data_for(main_date)
        self.refresh()

    def set_data_for(self, main_date):
        on , end = self.parent.on_date(),self.parent.end_date()
        self.data = [(rap.type_, rap.magasin, rap.produit, \
                        formatted_number(rap.nbr_carton), \
                        formatted_number(rap.restant), \
                        rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                        .filter(Rapport.date_rapp.__ge__(on)) \
                        .filter(Rapport.date_rapp.__le__(end)) \
                        .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _(u"input"):
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
