#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from ui.common import TabPane, Qt


def tabbox(*args):
    """ adds a box with tab
    params:  (widget, title) title is the string """
    tab_widget = QtGui.QTabWidget()
    tab_widget.setMovable(True)
    tab_widget.setAutoFillBackground(True)
    #~ tab_widget.setTabShape(QtGui.QTabWidget.Triangular)
    #~ tab_widget.setTabPosition(QtGui.QTabWidget.West)

    for box, btitle in args:
        pane = TabPane()
        pane.addBox(box)
        tab_widget.addTab(pane, btitle)
    return tab_widget
