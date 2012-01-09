#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad


from datetime import datetime

from sqlalchemy import desc
from PyQt4 import QtGui, QtCore

from database import *
from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle
from util import raise_success, raise_error
from edit_produit import EditProduitViewWidget

class ProduitViewWidget(F_Widget):

    def __init__(self, produit="", parent=0, *args, **kwargs):
        super(ProduitViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle((u"Produits"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"La liste des produits"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(u"Table produits"))
        self.table_op = ProduitTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.libelle = QtGui.QLineEdit()
        self.nbre_piece = QtGui.QLineEdit()
        self.nbre_piece.setValidator(QtGui.QIntValidator())

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(u"Add produit"))

        editbox.addWidget(QtGui.QLabel((_(u"Designation"))), 0, 0)
        editbox.addWidget(self.libelle, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Nbre de piece"))), 0, 1)
        editbox.addWidget(self.nbre_piece, 1, 1)
        butt = QtGui.QCommandLinkButton((u"Enregistrer"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''
        if unicode(self.libelle.text()) != "":
            if unicode(self.nbre_piece.text()) != "":
                produit = Produit(unicode(self.libelle.text()), \
                                  int(self.nbre_piece.text()))
                session.add(produit)
                session.commit()
                self.libelle.clear()
                self.nbre_piece.clear()
                self.refresh()
                self.change_main_context(ProduitViewWidget)
                raise_success(u"Confirmation", u"Le produit %s "
                              u" à été bien enregistrer" % produit.libelle)
            else:
                raise_error(u"error", \
                            u"Donnez le nombre de pièce dans le carton")
        else:
            raise_error(u"error", u"Donnez le nom du produit")


class ProduitTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [u"Designation", u"Nbre de pièce", u"modification"]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        self.data = [(prod.libelle, prod.nbr_piece, "") \
                                    for prod in session.query(Produit).\
                                        order_by(desc(Produit.id)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 2:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/pencil.png"), "")
        return super(ProduitTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)
    def click_item(self, row, column, *args):
        modified_column = 2
        if column == modified_column:
            self.open_dialog(EditProduitViewWidget, modal=True, \
                                produit=session.query(Produit) \
                                .filter(Produit.libelle==self.data[row][0]).all()[0])
            self.parent.change_main_context(ProduitViewWidget)
        else:
            return
