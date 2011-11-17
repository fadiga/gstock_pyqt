#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad


from datetime import datetime

from sqlalchemy import desc
from PyQt4 import QtGui, QtCore

from database import *
from common import (F_Widget, F_PageTitle, F_TableWidget,
                                                F_BoxTitle)
from utils import raise_success, raise_error


class ProduitViewWidget(F_Widget):

    def __init__(self, produit="", parent=0, *args, **kwargs):
        super(ProduitViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle((u"Produits"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"La liste des produits"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(u"Table produits"))
        self.table_op = MagasinTableWidget(parent=self)
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
        butt = QtGui.QPushButton((u"Add"))
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
                raise_success(_(u"Confirmation"), _(u"Registered opération"))
            else:
                raise_error(_(u"error"), \
                            _(u"Donnez le nombre de pièce dans le carton"))
        else:
            raise_error(_(u"error"), _(u"Donnez le nom du produit"))


class MagasinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [(u"Designation"), (u"Nbre de piece")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        self.data = [(prod.libelle, prod.nbr_piece) \
                                    for prod in session.query(Produit).\
                                        order_by(desc(Produit.id)).all()]
