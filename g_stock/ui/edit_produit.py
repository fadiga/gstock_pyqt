#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui

from common import F_Widget, F_BoxTitle, Button
from util import raise_error, raise_success
from data_helper import update_rapport
from database import *

class EditProduitViewWidget(QtGui.QDialog, F_Widget):
    def __init__(self, produit, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(u"Modification")

        self.prod = produit
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(u"Voulez-vous modification?"))
        self.new_produit = QtGui.QLineEdit(self.prod.libelle)
        self.new_nbr_piece = QtGui.QLineEdit(str(self.prod.nbr_piece))
        self.new_nbr_piece.setValidator(QtGui.QIntValidator())
        editbox = QtGui.QGridLayout()
        editbox.addWidget(QtGui.QLabel("Nom du produit"), 0, 1)
        editbox.addWidget(self.new_produit, 0, 2)
        editbox.addWidget(QtGui.QLabel("Nombre de piece"), 1, 1)
        editbox.addWidget(self.new_nbr_piece, 1, 2)
        butt = Button(u"Enregistre la modification")
        butt.clicked.connect(self.edit_prod)
        cancel_but = Button(u"Cancel")
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 2, 1)
        editbox.addWidget(cancel_but, 2, 2)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_prod(self):
        produit = session.query(Produit)\
                         .filter(Produit.libelle==self.prod.libelle) \
                         .filter(Produit.nbr_piece==self.prod.nbr_piece)\
                         .all()[0]
        produit.libelle = str(self.new_produit.text())
        produit.nbr_piece = int(self.new_nbr_piece.text())
        session.add(produit)
        session.commit()
        self.cancel()
        raise_success(u"Confirmation", u"Le produit à été modifier")
