#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

import os
import sys
import locale
from PyQt4 import QtGui
from ui.window import F_Window
import tempfile
import subprocess


class PDFFileUnavailable(IOError):
    pass


def uopen_prefix(platform=sys.platform):

    if platform in ('win32', 'win64'):
        return 'cmd /c start'

    if 'darwin' in platform:
        return 'open'

    if platform in ('cygwin', 'linux') or \
       platform.startswith('linux') or \
       platform.startswith('sun') or \
       'bsd' in platform:
        return 'xdg-open'

    return 'xdg-open'


def uopen_file(filename):
    if not os.path.exists(filename):
        raise IOError(_(u"File %s is not available.") % filename)
    subprocess.call('%(cmd)s %(file)s' \
                    % {'cmd': uopen_prefix(), 'file': filename}, shell=True)


def get_temp_filename(extension=None):
    f = tempfile.NamedTemporaryFile(delete=False)
    if extension:
        fname = '%s.%s' % (f.name, extension)
    else:
        fname = f.name
    return fname


def raise_error(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title, \
                            message, QtGui.QMessageBox.Ok, \
                            parent=F_Window.window)
    box.setWindowOpacity(0.9)
    box.exec_()


def raise_success(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Information, title, \
                            message, QtGui.QMessageBox.Ok, \
                            parent=F_Window.window)
    box.setWindowOpacity(0.9)
    box.exec_()


def formatted_number(number):
    try:
        return locale.format("%d", number, grouping=True) \
                     .decode(locale.getlocale()[1])
    except:
        return "%s" % number
