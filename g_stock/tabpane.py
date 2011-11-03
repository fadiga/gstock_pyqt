#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad


from PyQt4 import QtGui
from ui.common import TabPane


def tabbox(box1, Box2):
    """ adds a box with tab """
    tab_widget = QtGui.QTabWidget()
    for heading in [_("Graphe"), _("Table")]:
            pane = TabPane()
            if heading == "Graphe":
                pass
            else:
                pane.addBox(Box2)
            tab_widget.addTab(pane, heading)
    return tab_widget
