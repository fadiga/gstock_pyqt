#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle


class by_magasinViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, magasin, parent=0, *args, **kwargs):

        super(by_magasinViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)
        F_PeriodHolder.__init__(self, *args, **kwargs)

        self.title = F_PageTitle(" ".join([u"Les rapports dans le magasin: ", \
                                                            magasin.name]))
        self.table = by_magasinTableWidget(magasin, parent=self, \
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


class by_magasinTableWidget(F_TableWidget):

    def __init__(self, magasin, parent, period, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Type"), _(u"Produit"), \
                       _(u"Nombre de carton"), _(u"Carto Restant"), \
                       _(u"Date")]
        self.mag = magasin
        self.set_data_for(period)
        self.refresh(True)

    def refresh_period(self, period):
        self.main_period = period
        self.set_data_for(period)
        self.refresh()

    def set_data_for(self, period):
        self.data = [(rap.type_, rap.produit, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                        for rap in session.query(Rapport)\
                                .filter(Rapport.magasin_id == self.mag.id)]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == "Entre":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), \
                                          _(u""))
        if column == 0 and self.data[row][0] == "Sortie":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), \
                                          _(u""))
        return super(by_magasinTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)

    def click_item(self, row, column, *args):
        produit_column = 1
        if column == produit_column:
            from by_produit import by_produitViewWidget
            self.parent.change_main_context(by_produitViewWidget, \
                                    produit=self.data[row][produit_column])
        else:
            return
