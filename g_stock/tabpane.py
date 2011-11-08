#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad


from PyQt4 import QtGui
from ui.common import TabPane


def tabbox(*args):
    """ adds a box with tab
    params:  (widget, title) title is the string """
    ongles = args
    tab_widget = QtGui.QTabWidget()

    for el in ongles:
        pane = TabPane()
        pane.addBox(el[0])
        tab_widget.addTab(pane, el[1])
    return tab_widget
