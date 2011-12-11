#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4 import QtGui, QtCore
from common import F_Widget
from magasins import MagasinViewWidget
from tools.exports import export_database_as_file, export_database_as_excel

class MenuBar(QtGui.QMenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        #Menu File
        file_ = self.addMenu((u"&File"))

        # Print
        print_ = QtGui.QAction((u"Print"), self)
        print_.setShortcut("Ctrl+P")
        self.connect(print_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_print)
        file_.addAction(print_)
        # Export
        export = file_.addMenu((u"&Export data"))
        export.addAction((u"Backup Database"), self.goto_export_db)
        export.addAction((u"In an Excel file"),\
                                        self.goto_export_excel)
        # magasin
        
        magasin = QtGui.QAction((u"Nouveau magasin"), self)
        magasin.setShortcut("Ctrl+M")
        self.connect(magasin, QtCore.SIGNAL("triggered()"),\
                                            self.addstore)
        file_.addAction(magasin)
        # Exit
        exit = QtGui.QAction((u"Exit"), self)
        exit.setShortcut("Ctrl+Q")
        exit.setToolTip(("Exit application"))
        self.connect(exit, QtCore.SIGNAL("triggered()"), \
                                         self.parentWidget(), \
                                         QtCore.SLOT("close()"))
        file_.addAction(exit)
        # Menu aller à

        #Menu Aide
        help = self.addMenu((u"Help"))
        help.addAction(QtGui.QIcon('images/about.png'), "A propos", self.goto_about)

    #Refresh the menu bar to enabled or disabled the delete menu
    def refresh(self):
        pass

    #Print
    def goto_print(self):
        pass

    #Export the database.
    def goto_export_db(self):
        pass

    def goto_export_excel(self):
        pass

    def addstore(self):
        self.change_main_context(MagasinViewWidget)
        
    #Export the database.
    def goto_export_db(self):
        export_database_as_file()

    def goto_export_excel(self):
        export_database_as_excel()
        
    #About

    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self, (u"A propos"), \
                                 (u"G_stock gestion de stock\n\n" \
                                    "Developpeur: Ibrahima Fadiga, \n"\
                                    u"© 2011 fad service s.à.r.l\n" \
                                    u"Bamako (Mali)\n" \
                                    u"Tel: (223) 76 43 38 90\n" \
                                    u"E-mail: ibfadiga@gmail.com"))
