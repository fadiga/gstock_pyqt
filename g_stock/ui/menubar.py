#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4 import QtGui, QtCore

from common import F_Widget
from magasins import MagasinViewWidget
from by_period import by_periodViewWidget
from tools.exports import export_database_as_file, export_database_as_excel


class MenuBar(QtGui.QMenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        #Menu File
        file_ = self.addMenu(u"&Fichier")

        # Print
        print_ = QtGui.QAction((u"Print"), self)
        print_.setShortcut("Ctrl+P")
        self.connect(print_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_print)
        file_.addAction(print_)
        # Export
        export = file_.addMenu((u"&Export data"))
        export.addAction((u"Savegarde de la Database"), self.goto_export_db)
        export.addAction((u"Export db en Excel"),\
                                        self.goto_export_excel)

        # Exit
        exit_ = QtGui.QAction((u"Quiter"), self)
        exit_.setShortcut("Ctrl+Q")
        exit_.setToolTip(("Quiter l'application"))
        self.connect(exit_, QtCore.SIGNAL("triggered()"), \
                                         self.parentWidget(), \
                                         QtCore.SLOT("close()"))
        file_.addAction(exit_)
        # Menu aller à
        goto_ = self.addMenu((u"Aller à"))
        # magasin
        magasin = QtGui.QAction((u"Nouveau magasin"), self)
        magasin.setShortcut("Ctrl+M")
        self.connect(magasin, QtCore.SIGNAL("triggered()"),\
                                            self.addstore)
        goto_.addAction(magasin)
        # Rapport periodique
        rap_p = QtGui.QAction((u"Rapport periodique"), self)
        rap_p.setShortcut("Ctrl+T")
        self.connect(rap_p, QtCore.SIGNAL("triggered()"),\
                                            self.report_period)
        goto_.addAction(rap_p)

        #Menu Aide
        help_ = self.addMenu((u"Aide"))
        help_.addAction(QtGui.QIcon('images/help.png'), "Aide", self.goto_help)
        help_.addAction(QtGui.QIcon('images/about.png'), "A propos", self.report_period)

    #Refresh the menu bar to enabled or disabled the delete menu
    def refresh(self):
        pass

    #Print
    def goto_print(self):
        pass

    #Rapport periodique.
    def report_period(self):
        self.change_main_context(by_periodViewWidget)


    def addstore(self):
        self.change_main_context(MagasinViewWidget)

    #Export the database.
    def goto_export_db(self):
        export_database_as_file()

    def goto_export_excel(self):
        export_database_as_excel()

    #Aide
    def goto_help(self):
        mbox = QtGui.QMessageBox.about(self, (u"Aide"), \
                                 (u"Bien d'aide appele Fad"))

    #About
    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self, (u"A propos"), \
                                 (u"G_stock gestion de stock\n\n" \
                                    "Developpeur: Ibrahima Fadiga, \n"\
                                    u"© 2011 fad service s.à.r.l\n" \
                                    u"Bamako (Mali)\n" \
                                    u"Tel: (223) 76 43 38 90\n" \
                                    u"E-mail: ibfadiga@gmail.com"))
