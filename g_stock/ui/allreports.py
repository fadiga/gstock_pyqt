#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from sqlalchemy import desc

from database import Rapport, session
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle
from by_magasin import By_magasinViewWidget
from by_produit import By_produitViewWidget
from data_helper import last_mouvement_report


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

        self.header = [(u"Store No."), _(u"Product"), \
                       _(u"Number of carton"), _(u"Remaining"), \
                       _(u"Date")]
        self.set_data_for(main_date)

        self.setDisplayTotal(True, column_totals={3: None}, \
                             label=_(u"TOTALS"))
        self.refresh(True)
        # self.setColumnWidth(0, 20)

    def refresh_period(self, main_date):
        """ """
        self._reset()
        self.set_data_for(main_date)
        self.refresh()

    def set_data_for(self, main_date):
        on , end = self.parent.on_date(),self.parent.end_date()
        rapports = last_mouvement_report(on, end)
        self.data = [(rap.magasin, rap.produit, \
                     rap.nbr_carton, rap.restant,
                     rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                     for rap in rapports]

    def click_item(self, row, column, *args):
        magsin_column = 0
        produit_column = 1
        if column == magsin_column:
            self.parent.change_main_context(By_magasinViewWidget,
                                    magasin=self.data[row][magsin_column])
        if column == produit_column:
            self.parent.change_main_context(By_produitViewWidget,
                                    produit=self.data[row][produit_column])
        else:
            return
