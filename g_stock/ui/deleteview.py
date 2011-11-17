#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import F_Widget, F_TableWidget, F_PeriodHolder, F_PageTitle
from utils import raise_error, raise_success
from database import *


class deleteViewWidget(QtGui.QDialog, F_Widget):

    def __init__(self, report, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle((u"Suppression"))
        self.title = F_PageTitle(u"Suppression")
        self.op = report
        self.title.setText(_(u"Confirmation de la suppresion"))
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(self.title)
        report_hbox = QtGui.QGridLayout()

        report_hbox.addWidget(QtGui.QLabel(" ".\
                        join(["Le produit ", \
                        self.op.produit.libelle, u" qui se trouve dans ", \
                        self.op.magasin.name, u"enregister le", \
                        self.op.date_rapp.strftime('%x %Hh:%Mmn')])), 0, 0)
        #delete and cancel hbox
        button_hbox = QtGui.QHBoxLayout()

        #Delete Button widget.
        delete_but = QtGui.QPushButton(_(u"Delete operation"))
        button_hbox.addWidget(delete_but)
        delete_but.clicked.connect(self.delete)
        #Cancel Button widget.
        cancel_but = QtGui.QPushButton(_(u"Cancel"))
        button_hbox.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)

        #Create the QVBoxLayout contenaire.
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(report_hbox)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def delete(self):
        session.delete(self.op)
        session.commit()
        self.cancel()
        raise_success(u"Confirmation", \
                        " ".join(["Ce rapport conserne le produit ", \
                        self.op.produit.libelle, u" qui se trouve dans ", \
                        self.op.magasin.name, u"enregister le", \
                        self.op.date_rapp.strftime('%x %Hh:%Mmn'), \
                        u"A été supprimer"]))
