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
from data_helper import remaining

class G_rapportViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(G_rapportViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle((u"Gestion des rapports"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"Gestion des rapports"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(u"Table rapport"))
        self.table_op = MagasinTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.nbre_carton = QtGui.QLineEdit()
        self.nbre_carton.setValidator(QtGui.QIntValidator())

        self.date_ = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
        self.date_.setDisplayFormat("dd/MM/yyyy")
        self.time = QtGui.QDateTimeEdit(QtCore.QTime.currentTime())
        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(u"Add rapport"))

        self.liste_type = [_("Entre"), _("Sortie")]
        #Combobox widget
        self.box_type = QtGui.QComboBox()
        for index in self.liste_type:
            self.box_type.addItem(u'%(type)s' % {'type': index})
        #Combobox widget
        self.liste_magasin = session.query(Magasin).order_by(desc(Magasin.id)).all()
        self.box_mag = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_magasin)):
            op = self.liste_magasin[index]
            sentence = _(u"%(name)s")  % {'name': op.name}
            self.box_mag.addItem(sentence, QtCore.QVariant(op.id))
        #Combobox widget
        self.liste_produit = session.query(Produit).order_by(desc(Produit.id)).all()
        self.box_prod = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_produit)):
            op = self.liste_produit[index]
            sentence = _(u"%(libelle)s")  % {'libelle': op.libelle}
            self.box_prod.addItem(sentence, QtCore.QVariant(op.id))

        editbox.addWidget(QtGui.QLabel((_(u"Type"))), 0, 0)
        editbox.addWidget(self.box_type, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Magasin"))), 0, 1)
        editbox.addWidget(self.box_mag, 1, 1)
        editbox.addWidget(QtGui.QLabel((_(u"Produit"))), 0, 2)
        editbox.addWidget(self.box_prod, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Nbre carton"))), 0, 3)
        editbox.addWidget(self.nbre_carton, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 4)
        editbox.addWidget(self.date_, 1, 4)
        butt = QtGui.QPushButton((u"Add"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 5)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''
        type_ = self.liste_type[self.box_type.currentIndex()]
        magasin = self.liste_magasin[self.box_mag.currentIndex()]
        produit = self.liste_produit[self.box_prod.currentIndex()]
        nbre_carton = self.nbre_carton.text()
        date_ = self.date_.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        datetime_ = datetime(int(year), int(month), int(day), dt.hour, \
                                    dt.minute, dt.second, dt.microsecond)

        if unicode(self.nbre_carton.text()) != "" :
            r = remaining(type_,  nbre_carton, magasin.id, produit.id)
            if r[0] == None:
                raise_error(_(u"error"), _(r[1]))
            else:
                report = Rapport(unicode(type_), int(nbre_carton), datetime_)
                report.magasin = magasin
                report.produit = produit
                report.restant = r[0]
                session.add(report)
                session.commit()
                self.nbre_carton.clear()
                self.refresh()
                self.change_main_context(G_rapportViewWidget)
                raise_success(_(u"Confirmation"), _(u"Registered opération"))
        else:
            raise_error(_(u"error"), _(u"Donnez le nbre de carton"))


class MagasinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Type"), _(u"Magasins"), _(u"Produits"), \
                        _(u"Nbre de carton"), _(u"Restant"), _(u"Date")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        self.data = [(rap.type_, rap.magasin, rap.produit, \
                        rap.nbr_carton, rap.restant, rap.date_rapp.strftime(u'%x %Hh:%Mmn')) \
                        for rap in session.query(Rapport).\
                        order_by(desc(Rapport.id)).all()]