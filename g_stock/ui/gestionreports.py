#!usr/bin/env python
# -*- coding: utf-8 -*-
#maintainer: Fadiga


from datetime import datetime

from sqlalchemy import desc
from PyQt4 import QtGui, QtCore

from database import *
from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle, \
                                                    Button, FormatDate
from util import raise_success, raise_error, formatted_number
from magasins import MagasinViewWidget
from produits import ProduitViewWidget
from data_helper import remaining
from deleteview import DeleteViewWidget
from allreports import AllreportsViewWidget
from by_magasin import By_magasinViewWidget
from by_produit import By_produitViewWidget
from edit_report import EditReportViewWidget


class G_reportViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(G_reportViewWidget, self).__init__(parent=parent,\
                                                        *args, **kwargs)
        self.setWindowTitle(_(u"Management reports"))
        vbox = QtGui.QVBoxLayout()

        tablebox = QtGui.QVBoxLayout()
        tablebox.addWidget(F_BoxTitle(_(u"Table rapports")))
        self.table_op = MagasinTableWidget(parent=self)
        tablebox.addWidget(self.table_op)

        self.nbr_carton = QtGui.QLineEdit()
        self.nbr_carton.setDragEnabled(True)
        self.nbr_carton.setValidator(QtGui.QIntValidator())

        self.date_ = FormatDate(QtCore.QDate.currentDate())
        self.date_.setFont(QtGui.QFont("Courier New", 10, True))

        self.time = QtGui.QDateTimeEdit(QtCore.QTime.currentTime())
        formbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        formbox.addWidget(F_BoxTitle(_(u"add report")))

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
            sentence = u"%(name)s" % {'name': op.name}
            self.box_mag.addItem(sentence, QtCore.QVariant(op.id))
        #Combobox widget
        self.liste_produit = session.query(Produit)\
                                    .order_by(desc(Produit.id)).all()
        self.box_prod = QtGui.QComboBox()
        for index in xrange(0, len(self.liste_produit)):
            op = self.liste_produit[index]
            sentence = _(u"%(libelle)s") % {'libelle': op.libelle}
            self.box_prod.addItem(sentence, QtCore.QVariant(op.id))

        editbox.addWidget(QtGui.QLabel(_(u"Type")), 0, 0)
        editbox.addWidget(self.box_type, 1, 0)
        editbox.addWidget(QtGui.QLabel(_(u"Store")), 0, 1)
        editbox.addWidget(self.box_mag, 1, 1)
        editbox.addWidget(QtGui.QLabel(_(u"Product")), 0, 2)
        editbox.addWidget(self.box_prod, 1, 2)
        editbox.addWidget(QtGui.QLabel((_(u"Number of carton "))), 0, 3)
        editbox.addWidget(self.nbr_carton, 1, 3)
        editbox.addWidget(QtGui.QLabel((_(u"Date"))), 0, 4)
        editbox.addWidget(self.date_, 1, 4)
        butt = Button(_(u"Save"))
        butt.clicked.connect(self.add_operation)
        editbox.addWidget(butt, 1, 5)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        self.setLayout(vbox)

    def refresh(self):
        self.table_op.refresh()

    def add_operation(self):
        ''' add operation '''
        type_ = self.box_type.currentIndex()
        magasin = self.liste_magasin[self.box_mag.currentIndex()]
        produit = self.liste_produit[self.box_prod.currentIndex()]
        nbr_carton = self.nbr_carton.text()
        date_ = self.date_.text()
        day, month, year = date_.split('/')
        dt = datetime.now()
        datetime_ = datetime(int(year), int(month), int(day), int(dt.hour),
                             int(dt.minute), int(dt.second), int(dt.microsecond))

        if unicode(self.nbr_carton.text()) != "":
            r = remaining(type_,  nbr_carton, magasin.id, produit.id)
            if r[0] == None:
                raise_error(_(u"error"), r[1])
            else:
                report = Rapport(unicode(type_), int(nbr_carton), datetime_)
                report.magasin = magasin
                report.produit = produit
                report.restant = r[0]
                session.add(report)
                session.commit()
                self.nbr_carton.clear()
                self.table_op.refresh_()
                raise_success(_(u"Confirmation"), _(u"Registered operation"))
        else:
            raise_error(_(u"error"), _(u"Donnez le nbre de carton"))


class MagasinTableWidget(F_TableWidget):
    """ """

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [u" ", _(u"Store"), _(u"Product"), \
                             _(u"Number of carton"), _(u"Remaining"), u" ", \
                             _(u"Date"), _(u"Edit"), _(u"Delete")]
        self.set_data_for()
        self.refresh(True)
        #je cache la 5 eme colonne
        self.hideColumn(5)
        self.setColumnWidth(0, 20)

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(rap.type_, rap.magasin, rap.produit, \
                        formatted_number(rap.nbr_carton), \
                        formatted_number(rap.restant), \
                        rap.date_rapp, \
                        rap.date_rapp.strftime(u'%x %Hh:%Mmn'), "", "") \
                        for rap in session.query(Rapport) \
                        .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0 and self.data[row][0] == _("input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), u"")
        if column == 0 and self.data[row][0] == _("inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), u"")
        if column == 7:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/pencil.png"), u"")
        if column == 8:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/del.png"), u"")
        return super(MagasinTableWidget, self)\
                                            ._item_for_data(row, column, \
                                                        data, context)

    def click_item(self, row, column, *args):
        magsin_column = 1
        produit_column = 2
        modified_column = 7
        del_column = 8
        if column == magsin_column:
            self.parent.change_main_context(By_magasinViewWidget, \
                                    magasin=self.data[row][magsin_column])
        if column == produit_column:
            self.parent.change_main_context(By_produitViewWidget, \
                                    produit=self.data[row][produit_column])
        if column == modified_column:
            self.open_dialog(EditReportViewWidget, modal=True,\
                             report=session.query(Rapport)\
                             .filter(Rapport.date_rapp == self \
                             .data[row][5]).all()[0])
            self.parent.change_main_context(G_reportViewWidget)

        if column == del_column:
            self.open_dialog(DeleteViewWidget, modal=True,\
                             report=session.query(Rapport)\
                             .filter(Rapport.date_rapp == self \
                             .data[row][5]).all()[0])
            self.parent.change_main_context(G_reportViewWidget)
        else:
            return
