#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from PyQt4 import QtCore

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle


class by_produitViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, produit, parent=0, *args, **kwargs):

        super(by_produitViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)
        F_PeriodHolder.__init__(self, *args, **kwargs)

        self.title = F_PageTitle(" ".join([u"Les rapports dont le produit:", \
                                                        produit.libelle]))
        self.table = by_produitTableWidget(produit, parent=self, \
                                                period=self.main_period)
        # periods
        period = ""

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()


class by_produitTableWidget(F_TableWidget):

    def __init__(self, produit, parent, period, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), _(u"Magasin"), \
                       _(u"Nombre de carton"), _(u"Carto Restant"), \
                       _(u"Date")]
        self.prod = produit
        self.set_data_for(period)
        self.refresh(True)

    def refresh_period(self, period):
        self.main_period = period
        self.set_data_for(period)
        self.refresh()

    def set_data_for(self, period):
        self.data = [(rap.type_, rap.magasin, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                                .filter(Rapport.produit_id == self.prod.id)]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == "Entre":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), \
                                          _(u""))
        if column == 0 and self.data[row][0] == "Sortie":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), \
                                          _(u""))
        return super(by_produitTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)

    def click_item(self, row, column, *args):
        magsin_column = 1
        if column == magsin_column:
            from by_magasin import by_magasinViewWidget
            self.parent.change_main_context(by_magasinViewWidget, \
                                    magasin=self.data[row][magsin_column])
        else:
            return
