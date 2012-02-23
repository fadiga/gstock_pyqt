#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Maintainer: Fad

import sys
import gettext
import locale
import gettext_windows

from PyQt4 import QtGui

from ui.mainwindow import MainWindow
from ui.window import F_Window


def main():

    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('g_stock', localedir='locale', unicode=True)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    setattr(F_Window, 'window', window)
    window.show()
    #~ window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
