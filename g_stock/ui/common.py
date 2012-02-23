#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from datetime import *

from util import formatted_number

MAIN_WIDGET_SIZE = 950


class TabPane(QtGui.QTabBar):

    def __init__(self, parent=None):
        super(TabPane, self).__init__(parent)

    def addBox(self, box):
        self.setLayout(box)


class F_PageTitle(QtGui.QLabel):

    def __init__(self, *args, **kwargs):
        super(F_PageTitle, self).__init__(*args, **kwargs)
        self.setFont(QtGui.QFont("Times New Roman", 18))
        self.setAlignment(Qt.AlignCenter)


class F_BoxTitle(QtGui.QLabel):

    def __init__(self, *args, **kwargs):
        super(F_BoxTitle, self).__init__(*args, **kwargs)
        self.setFont(QtGui.QFont("Times New Roman", 14))
        self.setAlignment(Qt.AlignCenter)


class Button(QtGui.QCommandLinkButton):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setCheckable(True)


class Button_save(QtGui.QCommandLinkButton):

    def __init__(self, *args, **kwargs):
        super(Button_save, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setCheckable(True)
        self.setIcon(QtGui.QIcon.fromTheme('save',
                                           QtGui.QIcon('images/save.png')))


class Button_export(QtGui.QCommandLinkButton):

    def __init__(self, *args, **kwargs):
        super(Button_export, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setIcon(QtGui.QIcon.fromTheme('xls',
                                           QtGui.QIcon('images/xls.png')))
        self.setCheckable(True)


class FormatDate(QtGui.QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super(FormatDate, self).__init__(*args, **kwargs)
        self.setDisplayFormat(_(u"dd/MM/yyyy"))
        self.setCalendarPopup(True)


class FormLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)


class IntLineEdit(QtGui.QLineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QIntValidator(0, 100000, self))


class F_Widget(QtGui.QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.setMaximumWidth(MAIN_WIDGET_SIZE)

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.parentWidget()\
                          .change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, \
                                               modal=modal, *args, **kwargs)


class F_TableWidget(QtGui.QTableWidget, F_Widget):

    def __init__(self, parent, *args, **kwargs):

        QtGui.QTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self._data = []
        self._header = []
        self._display_total = False
        self._column_totals = {}
        self._total_label = _(u"TOTAL")

        self.parent = parent

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.cellClicked.connect(self.click_item)

        #~ self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setFont(QtGui.QFont("Times New Roman", 11))
        # style au tr
        self.setStyleSheet("color: #2C2C2C;")
        # enable sorting
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

    def setdata(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._data = value

    def getdata(self):
        return self._data

    data = property(getdata, setdata)

    def setheader(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._header = value

    def getheader(self):
        return self._header

    header = property(getheader, setheader)

    def _reset(self):
        for index in range(self.rowCount(), -1, -1):
            self.removeRow(index)

    def sort(self, Ncol, order):
        """ Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def refresh(self, resize=False):
        if not self.data or not self.header:
            return

        # increase rowCount by one if we have to display total row
        rc = self.data.__len__()
        if self._display_total:
            rc += 1
        self.setRowCount(rc)
        self.setColumnCount(self.header.__len__())
        self.setHorizontalHeaderLabels(self.header)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                ui_item = self._item_for_data(n, m, item, row)
                if isinstance(ui_item, QtGui.QTableWidgetItem):
                    self.setItem(n, m, ui_item)
                elif isinstance(ui_item, QtGui.QWidget):
                    self.setCellWidget(n, m, ui_item)
                else:
                    self.setItem(QtGui.QTableWidgetItem(u"%s" % ui_item))
                m += 1
            n += 1

        self._display_total_row()

        self.extend_rows()

        # only resize columns at initial refresh
        if resize:
            self.resizeColumnsToContents()

    def extend_rows(self):
        """ called after cells have been created/refresh.

            Use for adding/editing cells """
        pass

    def _item_for_data(self, row, column, data, context=None):
        ''' returns QTableWidgetItem or QWidget to add to a cell '''
        return QtGui.QTableWidgetItem(self._format_for_table(data))

    def _display_total_row(self, row_num=None):
        ''' adds the total row at end of table '''

        # display total row at end of table
        if self._display_total:

            if not row_num:
                row_num = self.data.__len__()

            # spans columns up to first data one
            # add label inside
            label_item = QtGui.QTableWidgetItem(u"%s" % self._total_label)
            label_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row_num, 0, label_item)
            self.setSpan(row_num, 0, 1, self._column_totals.keys()[0])
            # calculate total for each total column
            # if desired
            for index, total in self._column_totals.items():
                if not total:
                    total = sum([data[index] for data in self.data])
                item = QtGui.QTableWidgetItem(self._format_for_table(total))
                self.setItem(row_num, index, item)

    def setDisplayTotal(self, display=False, column_totals={}, label=None):
        """ adds an additional row at end of table

        display: bool wheter of not to display the total row
        column_totals: an hash indexed by column number
                       providing data to display as total or None
                       to request automatic calculation
        label: text of first cell (spaned up to first index)
        Example call:
            self.setDisplayTotal(True, \
                                 column_totals={2: None, 3: None}, \
                                 label="TOTALS") """

        self._display_total = display
        self._column_totals = column_totals
        if label:
            self._total_label = label

    def _format_for_table(self, value):
        """ formats input value for string in table widget """
        if isinstance(value, basestring):
            return value

        if isinstance(value, (int, float, long)):
            return formatted_number(value)

        return u"%s" % value

    def click_item(self, row, column, *args):
        pass


class F_PeriodHolder(object):

    def __init__(self, main_date=date.today(), *args, **kwargs):

        self.main_date = main_date
        self.periods_bar = self.gen_bar_for(self.main_date)

    def gen_bar_for(self, main_date):
        return F_PeriodTabBar(parent=self, main_date=self.main_date)

    def change_period(self, main_date):
        self.main_date = main_date

    def getmain_date(self):
        return self._main_date

    def setmain_date(self, value):
        self._main_date = value

    def on_date(self):
        return date(self._main_date.year, 01, 01)

    def end_date(self):
        return date(self._main_date.year, 12, 31)

    main_date = property(getmain_date, setmain_date)


class F_PeriodTabBar(QtGui.QTabBar):

    def __init__(self, parent, main_date, *args, **kwargs):

        super(F_PeriodTabBar, self).__init__(*args, **kwargs)

        for i in range(0, 3):
            self.addTab('%s' % i)
        self.set_data_from(main_date)
        self.build_tab_list()
        self.currentChanged.connect(self.changed_period)

    def set_data_from(self, period):

        self.main_date = period
        prev = self.main_date - timedelta(365)
        next_ = self.main_date + timedelta(365)
        self.periods = [prev, self.main_date, next_]

    def build_tab_list(self):
        for index, period in enumerate(self.periods):
            self.setTabText(index, str(period.strftime('%Y')))
            #~ self.setTabToolTip(index, str(period.strftime('%Y')))
        self.setTabTextColor(1, QtGui.QColor('darkBlue'))
        self.setCurrentIndex(1)

    def changed_period(self, index):
        if index == -1 or index == 1:
            return False
        else:
            np = self.periods[index]
            self.set_data_from(np)
            self.build_tab_list()
            self.parentWidget().main_date = np
            self.parentWidget().change_period(np)
