#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from PyQt4 import QtGui
from sqlalchemy import desc

from util import get_temp_filename, formatted_number
from database import Rapport, session
from data_helper import alerte_report, last_mouvement_report
from tabpane import tabbox
from common import F_Widget, F_PageTitle, F_TableWidget, F_BoxTitle


class DashbordViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DashbordViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)
        vbox = QtGui.QVBoxLayout()
        box_left = QtGui.QHBoxLayout()
        box_rigth = QtGui.QHBoxLayout()
        table_etat = QtGui.QVBoxLayout()
        table_alert = QtGui.QVBoxLayout()
        tablebox_dern_op = QtGui.QVBoxLayout()

        self.title = F_PageTitle(_("Dashboard"))

        self.title_alert = F_BoxTitle(_(u"The list of products that the  "
                                        u"rest is <100 cartons"))
        self.title_dern_op = F_BoxTitle(_(u"Table last operations"))

        self.title_etat = F_BoxTitle(_(u"Les stocks actual"))

        self.table_alert = Alert_TableWidget(parent=self)
        self.table_dern_op = Dern_opTableWidget(parent=self)
        self.table_etat = EtatTableWidget(parent=self)

        vbox.addWidget(self.title)
        table_etat.addWidget(self.title_etat)
        table_etat.addWidget(self.table_etat)

        table_alert.addWidget(self.title_alert)
        table_alert.addWidget(self.table_alert)

        tablebox_dern_op.addWidget(self.title_dern_op)
        tablebox_dern_op.addWidget(self.table_dern_op)
        tab_widget = tabbox((table_etat, _(u"Etat")),
                            (table_alert, _(u"Product warning")),
                            (tablebox_dern_op,  _(u"The last operations")))

        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


class EtatTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Store"), _(u"Product"), _(u"Remaining"), \
                       _(u"Date")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ """
        self.data = [(op.magasin, op.produit, formatted_number(op.restant),
                      op.date_rapp.strftime(_(u'%x %Hh:%Mmn')))
                     for op in last_mouvement_report()]


class Alert_TableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [_(u"Store"), _(u"Product"), _(u"Quantity"), \
                                      _(u"Remaining"), _(u"Date")]
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ """
        self.data = [(op.magasin, op.produit,\
                     formatted_number(op.nbr_carton), \
                     formatted_number(op.restant), \
                     op.date_rapp.strftime(_(u'%x %Hh:%Mmn')))
                     for op in alerte_report()]


class Dern_opTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.header = [u" ", _(u"Store"), _(u"Product"), _(u"Quantity"), \
                                            _(u"Remaining"), _(u"Date")]
        self.set_data_for()
        self.refresh(True)
        self.setColumnWidth(0, 20)

    def set_data_for(self):
        """ """
        self.data = [(op.type_, op.magasin, op.produit,\
                     formatted_number(op.nbr_carton), \
                     formatted_number(op.restant), \
                     op.date_rapp.strftime(_(u'%x %Hh:%Mmn'))) \
                     for op in session.query(Rapport)\
                        .order_by(desc(Rapport.date_rapp)).all()]

    def _item_for_data(self, row, column, data, context=None):

        if column == 0 and self.data[row][0] == _(u"input"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/In.png"), u"")
        if column == 0 and self.data[row][0] == _(u"inout"):
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/Out.png"), u"")
        return super(Dern_opTableWidget, self)._item_for_data(row, column, \
                                                                data, context)
