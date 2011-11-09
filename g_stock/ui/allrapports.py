
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import *
from data_helper import current_period
from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle
from gestionrapports import G_rapportViewWidget


class AllrapportsViewWidget(F_Widget, F_PeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):

        super(AllrapportsViewWidget, self).__init__(parent=parent, *args, **kwargs)
        F_PeriodHolder.__init__(self, *args, **kwargs)

        self.title = F_PageTitle(_(u"Tout les rapport"))

        self.table = RapportTableWidget(parent=self, period=self.main_period)

        # periods
        period = current_period()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def change_period(self, period):
        self.table.refresh_period(period)


class RapportTableWidget(F_TableWidget):

    def __init__(self, parent, period, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Magasin No."), _(u"Produit"), \
                        _(u"Nombre dde carton")]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.set_data_for(period)

        #~ self.refresh(True)

    def refresh_period(self, period):
        self.main_period = period
        self.set_data_for(period)
        self.refresh()

    def set_data_for(self, period):
        self.data = [(rap.magasin, rap.produit,rap.nbr_carton)
                for rap in session.query(Rapport).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 1:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/go-next.png"), \
                                          _(u"Operations"))
        return super(RapportTableWidget, self)\
                                    ._item_for_data(row, column, data, context)

    def click_item(self, row, column, *args):
        last_column = self.header.__len__() - 1
        if column != last_column:
            return
        try:
            self.parent.change_main_context(G_rapportViewWidget, \
                                        account=self.data[row][last_column], \
                                        period=self.parentWidget().main_period)
        except IndexError:
            pass
