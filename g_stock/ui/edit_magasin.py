#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import F_Widget, F_BoxTitle, Button
from util import raise_error, raise_success
from data_helper import update_rapport
from database import *


class EditMagasinViewWidget(QtGui.QDialog, F_Widget):
    def __init__(self, magasin, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Change"))

        self.mag = magasin.name
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(_(u"Do you want to change?")))
        self.new_magasin = QtGui.QLineEdit(self.mag)
        editbox = QtGui.QGridLayout()
        editbox.addWidget(QtGui.QLabel(_("Store Name")), 0, 1)
        editbox.addWidget(self.new_magasin, 0, 2)
        butt = Button(_(u"Records the change"))
        butt.clicked.connect(self.edit_mag)
        cancel_but = Button(_(u"Cancel"))
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 2, 1)
        editbox.addWidget(cancel_but, 2, 2)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_mag(self):
        magasin = session.query(Magasin).filter(Magasin.name == self.mag)\
                                        .all()[0]
        magasin.name = unicode(self.new_magasin.text())
        session.add(magasin)
        session.commit()
        self.cancel()
        raise_success(_(u"Confirmation"), _(u"The store has been changing"))
