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
        self.setWindowTitle(_(u"Change"))

        self.prod = produit
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(_(u"Do you want to change?")))
        self.new_produit = QtGui.QLineEdit(self.prod.libelle)
        self.new_nbr_piece = QtGui.QLineEdit(str(self.prod.nbr_piece))
        self.new_nbr_piece.setValidator(QtGui.QIntValidator())
        editbox = QtGui.QGridLayout()
        editbox.addWidget(QtGui.QLabel("Name of store"), 0, 1)
        editbox.addWidget(self.new_produit, 0, 2)
        editbox.addWidget(QtGui.QLabel(_("number of rooms")), 1, 1)
        editbox.addWidget(self.new_nbr_piece, 1, 2)
        butt = Button(_(u"Records the change"))
        butt.clicked.connect(self.edit_prod)
        cancel_but = Button(_(u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 2, 1)
        editbox.addWidget(cancel_but, 2, 2)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_prod(self):
        produit = session.query(Produit)\
                         .filter(Produit.libelle == self.prod.libelle) \
                         .filter(Produit.nbr_piece == self.prod.nbr_piece)\
                         .all()[0]
        lib = unicode(self.new_produit.text())
        nbr = self.new_nbr_piece.text()
        if lib != "":
            if unicode(nbr) != "":
                is_double = session.query(Produit)\
                          .filter(Produit.libelle==lib).all() == []
                if is_double:
                    produit = Produit(lib, int(nbr))
                    session.add(produit)
                    session.commit()
                    raise_success(_(u"Confirmation"), _(u"The product has been changing"))
                    self.cancel()
                else:
                    raise_error(_(u"error"), \
                                _(u"Ce produit existe déjà"))
            else:
                raise_error(_(u"error"), \
                            _(u"Give the room number in the box"))
        else:
            raise_error(_(u"Error"), _(u"Give the name of the product"))
