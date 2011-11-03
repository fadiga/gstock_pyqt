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


class MagasinViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(MagasinViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle((u"Magasins"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"La liste magasin"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(u"Table magasin"))
        self.table_op = MagasinTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.name = QtGui.QLineEdit()
        self.adresse = QtGui.QLineEdit()

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(u"Add opertion"))
        
        editbox.addWidget(QtGui.QLabel((_(u"Designation"))), 0, 0)
        editbox.addWidget(self.name, 1, 0)
        editbox.addWidget(QtGui.QLabel((_(u"Adresse du magasin"))), 0, 1)
        editbox.addWidget(self.adresse, 1, 1)
        butt = QtGui.QPushButton((u"Add"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 2)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''
        print unicode(self.name.text())
        if unicode(self.name.text()) != "":
            magasin = Magasin(unicode(self.name.text()), \
                              unicode(self.adresse.text()))
            session.add(magasin)
            session.commit()
            self.name.clear()
            self.adresse.clear()
            self.refresh()
            self.change_main_context(MagasinTableWidget)
            raise_success(_(u"Confirmation"), _(u"Registered opération"))
        else:
            raise_error(_(u"error"), _(u"Donnez le nom du magasin"))


class MagasinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [(u"Name"), (u"Adresse")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        self.data = [(mag.name, mag.adresse) for mag in session.query(Magasin).\
                        order_by(desc(Magasin.id)).all()]
