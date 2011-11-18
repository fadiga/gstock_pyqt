#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from PyQt4 import QtGui
from sqlalchemy import desc

from utils import get_temp_filename, formatted_number
from database import Magasin, Produit, Rapport, session
from tabpane import tabbox
from common import F_Widget, F_PageTitle, F_TableWidget, \
                                                F_BoxTitle


class DashbordViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DashbordViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        box_left = QtGui.QHBoxLayout()
        box_rigth = QtGui.QHBoxLayout()
        table_alert = QtGui.QVBoxLayout()
        tablebox_dern_op = QtGui.QVBoxLayout()

        self.title = F_PageTitle("Accuiel")
        self.title_alert = F_BoxTitle(_(u"Alerte sur les produits"))
        self.title_dern_op = F_BoxTitle(_(u"Table de dernière operations"))

        self.table_alert = Alert_TableWidget(parent=self)
        self.table_dern_op = Dern_opTableWidget(parent=self)

        vbox.addWidget(self.title)
        table_alert.addWidget(self.title_alert)
        table_alert.addWidget(self.table_alert)

        tablebox_dern_op.addWidget(self.title_dern_op)
        tablebox_dern_op.addWidget(self.table_dern_op)
        tab_widget = tabbox((table_alert, u"Alerte sur les produits"), \
                            (tablebox_dern_op, \
                                        u"Table de dernière operations"))

        vbox.addWidget(tab_widget)

        self.setLayout(vbox)


class Dern_opTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Type"), _(u"Magasin"), _(u"Produit"), \
                       _(u"Quantite"), u"Restant", (u"Date")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ """

        self.data = [(op.type_, op.magasin, op.produit,\
                     formatted_number(op.nbr_carton), \
                     formatted_number(op.restant), \
                     op.date_rapp.strftime(_(u'%x %Hh:%Mmn'))) \
                     for op in session.query(Rapport)\
                        .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == "Entre":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), \
                                          _(u""))
        if column == 0 and self.data[row][0] == "Sortie":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), \
                                          _(u""))
        return super(Dern_opTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)


class Alert_TableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Type"), _(u"Magasin"), _(u"Produit"), \
                       _(u"Quantite"), u"Restant", (u"Date")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ """

        self.data = [(op.type_, op.magasin, op.produit,\
                     formatted_number(op.nbr_carton), \
                     formatted_number(op.restant), \
                     op.date_rapp.strftime(_(u'%x %Hh:%Mmn')))
                     for op in session.query(Rapport)\
                        .filter(Rapport.restant <= 100)\
                        .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == "Entre":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), \
                                          _(u""))
        if column == 0 and self.data[row][0] == "Sortie":
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), \
                                          _(u""))
        return super(Alert_TableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)
