#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad


from sqlalchemy import asc

from PyQt4.QtGui import (QVBoxLayout, QAbstractItemView,
                         QGridLayout, QCheckBox)
from PyQt4.QtCore import SIGNAL, Qt, QDate

from database import session, Produit

from common import F_Widget, F_TableWidget, F_PageTitle, FormLabel, \
                        F_BoxTitle, Button_export, FormatDate, IntLineEdit
from utils.exports import export_command_as_excel


class CommandeViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(CommandeViewWidget, self).__init__(parent=parent, *args,
                                                                **kwargs)

        self.table = CommandeTableWidget(parent=self)

        self.title = F_PageTitle(_(u"Faire une Commande"))

        self.comm_date = FormatDate(QDate.currentDate())
        vbox = QVBoxLayout()

        self.afficherButton = Button_export(u"Afficher la commande")
        self.connect(self.afficherButton, SIGNAL('clicked()'),
                                          self.creat_commande)
        # Grid
        gridbox = QGridLayout()
        gridbox.addWidget(FormLabel(_(u"Date")), 0, 0)
        gridbox.addWidget(self.comm_date, 0, 1)
        gridbox.setColumnStretch(4, 5)
        gridbox.addWidget(self.afficherButton, 0, 2)
        vbox.addWidget(self.title)
        vbox.addLayout(gridbox)
        vbox.addWidget(F_PageTitle(_(u"Liste of Product")))
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def creat_commande(self):
        L = self.table.getTableItems()
        export_command_as_excel(L)


class CommandeTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Choix"), _(u"Quantity"), _(u"Product")]

        self.setEditTriggers(QAbstractItemView.EditTriggers(True))
        self.set_data_for()
        self.refresh(True)

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            # create check box as our editor.
            editor = QCheckBox()
            return editor
        return super(CommandeTableWidget, self)\
                     ._item_for_data(row, column, data, context)

    def getTableItems(self):
        n = self.rowCount()
        commad_list = []
        for i in range(n):
            liste_item = []
            item = self.cellWidget(i, 0)
            if item.checkState() == Qt.Checked:
                for o in range(1, 3):
                    liste_item.append(str(self.item(i, o).text()))
                commad_list.append(liste_item)
        return commad_list

    def set_data_for(self, *args):

        self.data = [("", "", prod.libelle)
                    for prod in session.query(Produit)\
                                       .order_by(asc(Produit.libelle)).all()]