#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore
from sqlalchemy import desc

from common import F_Widget,F_BoxTitle, F_PageTitle, Button, FormatDate
from util import raise_error, raise_success
from data_helper import update_rapport
from database import *


class EditReportViewWidget(QtGui.QDialog, F_Widget):

    def __init__(self, report, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Edited"))
        self.title = F_PageTitle(_(u"Voulez-vous modification?"))

        self.op = report
        vbox = QtGui.QVBoxLayout()

        self.nbre_carton = QtGui.QLineEdit(str(self.op.nbr_carton))
        self.nbre_carton.setValidator(QtGui.QIntValidator())

        self.date_ = FormatDate(QtCore.QDate(self.op.date_rapp))

        self.time = QtGui.QDateTimeEdit(QtCore.QTime.currentTime())
        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(_(u"Edit report")))

        #Combobox widget
        self.box_type = QtGui.QComboBox()
        self.box_type.addItem(_(u"input"))
        self.box_type.addItem(_(u"inout"))
        #Combobox widget
        self.liste_magasin = session.query(Magasin)\
                                    .order_by(desc(Magasin.id)).all()
        self.box_mag = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_magasin)):
            op = self.liste_magasin[index]
            sentence = _(u"%(name)s") % {'name': op.name}
            self.box_mag.addItem(sentence, QtCore.QVariant(op.id))
        #Combobox widget
        self.liste_produit = session.query(Produit)\
                                    .order_by(desc(Produit.id)).all()
        self.box_prod = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_produit)):
            op = self.liste_produit[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.libelle}
            self.box_prod.addItem(sentence, QtCore.QVariant(op.id))
            self.box_prod.setCurrentIndex(2)
        editbox.addWidget(QtGui.QLabel((_(u"Type"))), 0, 0)
        editbox.addWidget(self.box_type, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Store"))), 0, 1)
        editbox.addWidget(self.box_mag, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Product"))), 0, 2)
        editbox.addWidget(self.box_prod, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Nbre carton"))), 0, 3)
        editbox.addWidget(self.nbre_carton, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 4)
        editbox.addWidget(self.date_, 1, 4)
        butt = Button(_(u"Save"))
        butt.clicked.connect(self.edit_report)
        cancel_but = Button((u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 2, 3)
        editbox.addWidget(cancel_but, 2, 4)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_report(self):
        report = self.op
        report.type_ = ""
        report.magasin = ""
        report.produit = ""
        report.nbr_cartion = ""
        #~ session.add(report)
        #~ session.commit()
        #~ update_rapport(self.op)
        self.cancel()
        raise_success(u"Confirmation", \
                        " ".join(["Ce rapport conserne le produit ", \
                        self.op.produit.libelle, u" qui se trouve dans ", \
                        self.op.magasin.name, u"enregister le", \
                        self.op.date_rapp.strftime('%x %Hh:%Mmn'), \
                        u"A été supprimer"]))
