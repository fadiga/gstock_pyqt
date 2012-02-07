#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore
import thread
import time
from datetime import datetime

class REDEStatusBar(QtGui.QStatusBar):

    def __init__(self, parent):

        QtGui.QStatusBar.__init__(self, parent)

        self.showMessage(_(u"Welcome!" + " Fatoumata"), 10000)

        self.setWindowOpacity(0.78)
