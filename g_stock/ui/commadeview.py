#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from datetime import date, timedelta

from PyQt4.QtGui import (QVBoxLayout, QWidget, QApplication, QLineEdit,
                         QPushButton,QAbstractItemView, QGridLayout)
from PyQt4.QtGui import QListView, QStringListModel, QMessageBox
from PyQt4.QtCore import SIGNAL, Qt, QDate

from database import session, Produit
from common import F_Widget, F_TableWidget, F_PageTitle, FormLabel, \
                        F_BoxTitle, Button_export, FormatDate, IntLineEdit


class CommandeViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(CommandeViewWidget, self).__init__(parent=parent, *args, \
                                                                **kwargs)

        self.table = CommandeTableWidget(parent=self)
        self.title = F_BoxTitle(_(u"Faire une Commande"))

        self.comm_date = FormatDate(QDate.currentDate())
        vbox = QVBoxLayout()

        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.afficherButton = Button_export(u"Afficher la commande")
        self.connect(self.afficherButton, SIGNAL('clicked()'), self.clicSelection)
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
        self.refresh()

    def clicSelection(self):
        selection = self.table.selectionModel()#QItemSelectionModel
        listeSelections = selection.selectedIndexes() #QModelIndexList
        L = [unicode(s.data().toString()) for s in listeSelections]
        QMessageBox.information(self, u"Eléments sélectionnés", '<br>'.join(L))


class CommandeTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Product"), _(u"Quantity"), \
                       _(u"Prix U"), _(u"Montant")]

        self.set_data_for()
        self.refresh(True)

    def extend_rows(self):

        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 1)
        self.setSpan(nb_rows, 0, 1, 3)
        self.button = Button_export(_("Exporter"))
        self.button.released.connect(self.export_data)
        self.setCellWidget(nb_rows, 3, self.button)

    def export_data():
        print "export ok"

    def _item_for_data(self, row, column, data, context=None):
        if column != 0:
            line_edit = QLineEdit(u"%s" % data)
            line_edit.editingFinished.connect(self.changed_value)
            return line_edit


        return super(CommandeTableWidget, self)\
                     ._item_for_data(row, column, data, context)

    def changed_value(self, refresh=False):
        pass

    def set_data_for(self, *args):

        self.data = [(prod.libelle, "", "", "") \
                    for prod in session.query(Produit).all()]
