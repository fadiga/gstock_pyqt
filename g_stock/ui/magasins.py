#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fad


from datetime import datetime

from sqlalchemy import desc
from PyQt4 import QtGui, QtCore

from database import *
from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle
from util import raise_success, raise_error
from edit_magasin import EditMagasinViewWidget


class MagasinViewWidget(F_Widget):

    def __init__(self, magasin="", parent=0, *args, **kwargs):
        super(MagasinViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle((u"Magasins"))
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"La liste des magasins"))

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(u"Table magasin"))
        self.table_op = MagasinTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.name = QtGui.QLineEdit()

        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(u"Add opertion"))

        editbox.addWidget(QtGui.QLabel((_(u"Nom du magasin"))), 0, 0)
        editbox.addWidget(self.name, 1, 0)
        butt = QtGui.QCommandLinkButton((u"Enregistrer"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 1)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''

        if unicode(self.name.text()) != "":
            magasin = Magasin(unicode(self.name.text()))
            session.add(magasin)
            session.commit()
            self.name.clear()
            self.refresh()
            raise_success(_(u"Confirmation"), _(u"Registered opération"))
        else:
            raise_error(u"Erreur", u"Donnez le nom du magasin")
        self.change_main_context(MagasinViewWidget)


class MagasinTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [(u"Name"), (u"Modication")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        self.data = [(mag.name, "") for mag in session.query(Magasin).\
                                    order_by(desc(Magasin.id)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 1:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/pencil.png"), "")
        return super(MagasinTableWidget, self)._item_for_data(row, column, \
                                                        data, context)
    def click_item(self, row, column, *args):
        modified_column = 1
        if column == modified_column:
            self.open_dialog(EditMagasinViewWidget, modal=True, \
                                magasin=session.query(Magasin) \
                                .filter(Magasin.name==self.data[row][0]).all()[0])
            self.parent.change_main_context(MagasinViewWidget)
        else:
            return
