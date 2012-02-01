#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import F_Widget, F_PageTitle, Button
from util import raise_error, raise_success
from data_helper import update_rapport
from database import *


class DeleteViewWidget(QtGui.QDialog, F_Widget):

    def __init__(self, report, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)
        self.setWindowTitle(_(u"Delete Confirmation"))
        self.title = F_PageTitle(_(u"Do you want to delete?"))
        self.op = report
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(self.title)
        report_hbox = QtGui.QGridLayout()

        report_hbox.addWidget(QtGui.QLabel(_(u"The product %(product)s found"
                                             u" in %(store)s "
                                             u"save the %(date)s") %
                                            {"product": self.op.produit \
                                            .libelle, "store": self.op \
                                            .magasin.name, "date": self.op \
                                            .date_rapp \
                                            .strftime('%x %Hh:%Mmn')}), 0, 0)
        #delete and cancel hbox
        Button_hbox = QtGui.QHBoxLayout()

        #Delete Button widget.
        delete_but = Button(_(u"Deleted"))
        Button_hbox.addWidget(delete_but)
        delete_but.clicked.connect(self.delete)
        #Cancel Button widget.
        cancel_but = Button(_(u"Cancel"))
        Button_hbox.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)

        #Create the QVBoxLayout contenaire.
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(report_hbox)
        vbox.addLayout(Button_hbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def delete(self):
        session.delete(self.op)
        session.commit()
        update_rapport(self.op)
        self.cancel()
        raise_success(_(u"Confirmation"), _(u"Your report has been deleted"))
