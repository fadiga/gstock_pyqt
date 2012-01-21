#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from sqlalchemy import desc

from database import *
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle


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

        self.header = [u"", _(u"store"), \
                       _(u"Number of carton"), _(u"Remaining"), \
                       _(u"Date")]
        self.prod = produit
        self.set_data_for(main_date)
        self.refresh(True)

    def refresh_period(self, main_date):
        self._reset()
        self.set_data_for(main_date)
        self.refresh()

    def set_data_for(self, main_date):

        on , end = self.parent.on_date(),self.parent.end_date()
        self.data = [(rap.type_, rap.magasin, rap.nbr_carton, \
                      rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn'))
                      for rap in session.query(Rapport)\
                                .filter(Rapport.produit_id == self.prod.id)\
                                .filter(Rapport.date_rapp.__ge__(on)) \
                                .filter(Rapport.date_rapp.__le__(end)) \
                                .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _("input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), u"")
        if column == 0 and self.data[row][0] == _("inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), u"")
        return super(By_produitTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)

    def click_item(self, row, column, *args):
        magsin_column = 1
        if column == magsin_column:
            from by_magasin import By_magasinViewWidget
            self.parent.change_main_context(By_magasinViewWidget, \
                                    magasin=self.data[row][magsin_column])
        else:
            return
