#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui
from ui.common import TabPane


def tabbox(*args):
    """ adds a box with tab
    params:  (widget, title) title is the string """
    tab_widget = QtGui.QTabWidget()
    for box, btitle in args:
        pane = TabPane()
        pane.addBox(box)
        tab_widget.addTab(pane, btitle)
    return tab_widget
