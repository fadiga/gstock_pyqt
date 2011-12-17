#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import sys

from PyQt4 import QtGui, QtCore

from database import *
from dashboard import DashbordViewWidget
from magasins import MagasinViewWidget
from produits import ProduitViewWidget
from gestionreports import G_reportViewWidget
from allreports import AllreportsViewWidget
from menubar import MenuBar


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(900, 650)
        self.setWindowTitle(u"gestion de stock")
        self.setWindowIcon(QtGui.QIcon('images/mali.png'))

        self.toolbar = QtGui.QToolBar()
        self.toolbar.addAction(QtGui.QIcon('images/quiter.png'), \
                                                    "Quiter", self.goto_exit)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Accueil", self.accueil)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Produits", self.goto_produit)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Tous les rapports", \
                                                    self.goto_all_rapport)
        self.toolbar.addSeparator()
        self.toolbar.addAction("Gestion des rapports", \
                                                self.goto_gestion_rapport)

        self.addToolBar(self.toolbar)

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        self.change_context(DashbordViewWidget)

    def goto_exit(self):
        self.close()

    def accueil(self):
        self.setWindowTitle(u"Accueil")
        self.change_context(DashbordViewWidget)

    def goto_produit(self):
        self.setWindowTitle(u"Produits")
        self.change_context(ProduitViewWidget)

    def goto_all_rapport(self):
        self.setWindowTitle(u"Tous les Rapports")
        self.change_context(AllreportsViewWidget)

    def goto_gestion_rapport(self):
        self.setWindowTitle(u"Gestion Rapports")
        self.change_context(G_reportViewWidget)

    def change_context(self, context_widget, list_=[], *args, **kwargs):

        # instanciate context
        self.list_ = list_
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.exec_()
