#!/usr/bin/env python
# encoding=utf-8
# maintainer: fadiga

import time
from datetime import datetime

from PyQt4 import QtGui, QtCore


class GStatusBar(QtGui.QStatusBar):

    def __init__(self, parent):

        QtGui.QStatusBar.__init__(self, parent)

        self.showMessage(_(u"Welcome!") + (" Dans Gstock"), 10000)

        self.setWindowOpacity(0.78)
