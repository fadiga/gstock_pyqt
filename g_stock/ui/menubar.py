#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4 import QtGui, QtCore
from common import F_Widget


class MenuBar(QtGui.QMenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        # change icon so that it appears in About box
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        #Menu File
        file_ = self.addMenu((u"&File"))
        # Dele
        self.delete_ = QtGui.QAction(u"Delete an operation", self)
        self.connect(self.delete_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_delete_rapport)
        self.delete_.setEnabled(False)
        file_.addAction(self.delete_)

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
        help.addAction((u"About"), self.goto_about)

    #Refresh the menu bar to enabled or disabled the delete menu
    def refresh(self):
        pass

    #Print
    def goto_print(self):
        pass

    #Delete an operation.
    def goto_delete_rapport(self):
        pass

    #Export the database.
    def goto_export_db(self):
        pass

    def goto_export_excel(self):
        pass

    #list_of_balances
    def resumer(self):
        pass
    #About
    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self, (u"About ANM"), \
                          (u"ibfadiga@gmail.com \n" \
                            u"FADIGA IBRAHIMA"))
