#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from sqlalchemy import desc

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle
from data_helper import last_mouvement_report


class By_produitViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, produit, parent=0, *args, **kwargs):

        super(By_produitViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)
        F_PeriodHolder.__init__(self, *args, **kwargs)

        self.title = F_PageTitle(_(u"The reports of the product: %s") % \
                                                        produit.libelle)
        self.table = By_produitTableWidget(produit, parent=self, \
                                           main_date=self.main_date)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def change_period(self, main_date):
        self.table.refresh_period(main_date)


class By_produitTableWidget(F_TableWidget):

    def __init__(self, produit, parent, main_date, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"store"), \
                       _(u"Number of carton"), _(u"Remaining"), \
                       _(u"Date")]
        self.prod = produit
        self.set_data_for(main_date)

        self.setDisplayTotal(True, column_totals={2: None}, \
                             label=_(u"TOTALS"))
        self.refresh(True)

    def refresh_period(self, main_date):
        self._reset()
        self.set_data_for(main_date)
        self.refresh()

    def set_data_for(self, main_date):

        on , end = self.parent.on_date(),self.parent.end_date()

        rapports = last_mouvement_report(on, end, product=self.prod)
        self.data = [(rap.magasin, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                      for rap in rapports]

    def click_item(self, row, column, *args):
        magsin_column = 0
        if column == magsin_column:
            from by_magasin import By_magasinViewWidget
            self.parent.change_main_context(By_magasinViewWidget, \
                                    magasin=self.data[row][magsin_column])
        else:
            return
