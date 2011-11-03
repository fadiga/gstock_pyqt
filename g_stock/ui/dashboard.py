#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

from PyQt4 import QtGui
from sqlalchemy import desc

from utils import get_temp_filename, formatted_number
from database import Magasin, Produit, Rapport, session
from tabpane import (tabbox)
from common import (F_Widget, F_PageTitle, F_TableWidget,
                                                F_BoxTitle)


class DashbordViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DashbordViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()
        box_left = QtGui.QHBoxLayout()
        box_rigth = QtGui.QHBoxLayout()
        hbox_alert = QtGui.QVBoxLayout()

        box = QtGui.QListWidget()

        #All alerts

        tablebox_balance = QtGui.QVBoxLayout()
        tablebox_consumption = QtGui.QVBoxLayout()
        
        balance = _("Welcome")

        self.title = F_PageTitle(balance)
        self.title_alert = F_PageTitle(_(u"Alerte sur les produits"))
        self.title_box_balance = F_BoxTitle(_(u"Table de dernière operations"))
        self.title_box_consumption = F_BoxTitle(_(u"Table "))

        self.table_balance = BalanceTableWidget(parent=self)
        self.table_consumption = ConsumptionTableWidget(parent=self)

        pixmap_balance = QtGui.QPixmap("graph_banlance.png")
        label_b = QtGui.QLabel()
        label_b.setPixmap(pixmap_balance)
        box_left.addWidget(label_b)
        pixmap_cons = QtGui.QPixmap("graph_consumption.png")
        label_cons = QtGui.QLabel()
        label_cons.setPixmap(pixmap_cons)
        box_rigth.addWidget(label_cons)

        hbox_alert.addWidget(self.title_alert)
        hbox_alert.addWidget(box)
        
        vbox.addWidget(self.title)
        tablebox_balance.addWidget(self.title_box_balance)
        tablebox_balance.addWidget(self.table_balance)
        tablebox_consumption.addWidget(self.title_box_consumption)
        tablebox_consumption.addWidget(self.table_consumption)
        tab_widget1 = tabbox(box_left, tablebox_balance)
        tab_widget2 = tabbox(box_rigth, tablebox_consumption)

        hbox.addWidget(tab_widget1)
        #~ hbox.addWidget(tab_widget2)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_alert)

        self.setLayout(vbox)


class BalanceTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Type"),_(u"Magasin"), _(u"Produit"), \
                       _(u"Date"), _(u"quantite")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):

        self.data = [(op.type_, op.magasin, op.produit,\
                        op.date_rapp.strftime(_(u'%x %Hh:%Mmn')),\
                        formatted_number(op.nbr_carton),)\
                        for op in session.query(Rapport)\
                        .order_by(desc(Rapport.date_rapp)).all()]


class ConsumptionTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Date"), _(u"Consumption")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ """
        self.data = [(op.libelle, formatted_number(op.nbr_piece))
                            for op in session.query(Produit).all()]
