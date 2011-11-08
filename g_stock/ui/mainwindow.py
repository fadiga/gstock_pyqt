#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from PyQt4 import QtGui, QtCore

from database import *
from dashboard import DashbordViewWidget
from magasins import MagasinViewWidget
from produits import ProduitViewWidget
from gestionrapports import G_rapportViewWidget
from allrapports import AllrapportsViewWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(900, 650)
        self.setWindowTitle(u"gestion de stock")
        self.setWindowIcon(QtGui.QIcon('images/mali.png'))

        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(QtGui.QIcon('images/out.png'), "Exit", self.goto_exit)
        self.toolbar.addAction("Aceuil", self.aceuil)
        self.toolbar.addAction("Magasin", self.goto_magasin)
        self.toolbar.addAction("Tous les rapports", self.goto_all_rapport)
        self.toolbar.addAction("Produit", self.goto_produit)
        self.toolbar.addAction("Gestion des rapports", self.goto_gestion_rapport)
        self.toolbar.addAction(QtGui.QIcon('images/about.png'), "Help", self.goto_help)
        self.addToolBar(self.toolbar)
        self.change_context(DashbordViewWidget)

    def goto_help(self):
        mbox = QtGui.QMessageBox.about(self, _(u"About gestion de stock"), \
                          _(u"G_stock gestion de stock\n\n" \
                            "Developpeur: Ibrahima Fadiga, \n"\
                            u"© 2011 fad service s.à.r.l\n" \
                            u"Bamako (Mali)\n" \
                            u"Tel: (223) 76 43 38 90\n" \
                            u"E-mail: ibfadiga@gmail.com\n\n" ))

    def goto_exit(self):
        self.close()

    def aceuil(self):
        self.setWindowTitle(u"Aceuil")
        self.change_context(DashbordViewWidget)

    def goto_produit(self):
        self.setWindowTitle(u"Produits")
        self.change_context(ProduitViewWidget)

    def goto_magasin(self):
        self.setWindowTitle(u"Magasins")
        self.change_context(MagasinViewWidget)

    def goto_all_rapport(self):
        self.setWindowTitle(u"Tous les Rapports")
        self.change_context(AllrapportsViewWidget)

    def goto_gestion_rapport(self):
        self.setWindowTitle(u"Gestion Rapports")
        self.change_context(G_rapportViewWidget)


    def change_context(self, context_widget, *args, **kwargs):

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)