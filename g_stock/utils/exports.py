#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import os
import shutil
from datetime import datetime

from PyQt4 import QtGui, QtCore

import database
from database import *
from export_xls import write_xls, write_command_xls
from util import raise_success, raise_error


def export_database_as_file():
    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(),
                                    _(u"Sauvegarder la base de Donnée."),
                                    "%s.db" % datetime.now()\
                                                .strftime('%d-%m-%Y %Hh%M'),
                                    "*.db")
    if not destination:
        return

    try:
        shutil.copyfile(database.DB_FILE, destination)
        raise_success(u"Les données ont été exportées correctement.",
                      u"Conservez ce fichier précieusement car il "
                      u"contient toutes vos données.\n"
                      u"Exportez vos données régulièrement."
                      u"Database exported!")
    except IOError:
        raise_error(u"La base de données n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n"
                    u"Demandez de l'aide si le problème persiste.")


def export_database_as_excel():

    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(),
                                    _(u"Save Excel Export as..."),
                                    "%s.xls" % datetime.now()
                                    .strftime(u"%X %Hh%M"), "*.xls")
    if not destination:
        return
    try:
        write_xls(destination)
        raise_success(u"Les données ont été exportées correctement.",
                      u"Conservez ce fichier précieusement car il contient "
                      u"toutes vos données.\n\n"
                      u"Exportez vos données régulièrement.")
    except IOError:
        raise_error(u"La base de données n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n"
                    u"Demandez de l'aide si le problème persiste.")


def export_command_as_excel(comm):

    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(),
                                      _(u"Save Excel Export as..."),
                                    "%s.xls" % datetime.now()
                                        .strftime('%x %Hh%M'), "*.xls")
    if not destination:
        return
    try:
        write_command_xls(destination, comm)
        raise_success(_(u"Success"),
                      _(u"Les données ont été exportées correctement."))
    except IOError:
        raise_error(u"La commande n'a pas pu être exportée.",
                    u"Vérifiez le chemin de destination puis re-essayez.\n\n"
                    u"Demandez de l'aide si le problème persiste.")
