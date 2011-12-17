#!usr/bin/env python
# -*- coding= UTF-8 -*-
#maintainer: Fadiga

import xlwt
import StringIO
from datetime import date
from sqlalchemy import desc

from database import *


font_title = xlwt.Font()
font_title.name = 'Times New Roman'
font_title.bold = True
font_title.height = 19 * 0x14
font_title.underline = xlwt.Font.UNDERLINE_DOUBLE

font = xlwt.Font()
font.name = 'Times New Roman'
font.height = 12 * 0x14
font.bold = True

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

al = xlwt.Alignment()
al.horz = xlwt.Alignment.HORZ_CENTER
al.vert = xlwt.Alignment.VERT_CENTER
al1 = xlwt.Alignment()
al1.horz = xlwt.Alignment.HORZ_RIGHT

color = xlwt.Pattern()
color.pattern = xlwt.Pattern.SOLID_PATTERN
color.pattern_fore_colour = 23

pat2 = xlwt.Pattern()
pat2.pattern = xlwt.Pattern.SOLID_PATTERN
pat2.pattern_fore_colour = 0x01F

#styles
style_title = xlwt.XFStyle()
style_title.font = font_title
style_title.alignment = al

style_t_table = xlwt.XFStyle()
style_t_table.font = font
style_t_table.pattern = color
style_t_table.alignment = al
style_t_table.borders = borders

style2 = xlwt.XFStyle()
style2.borders = borders

style1 = xlwt.XFStyle()
style1.pattern = pat2
style1.borders = borders

style = xlwt.XFStyle()
style.alignment = al1

style_mag = xlwt.XFStyle()
style_mag.font = font
style_mag.alignment = al
style_mag.borders = borders
style_mag.pattern = color


def write_xls(file_name):
    ''' Export data '''
    # Principe
    # write((nbre ligne - 1), nbre colonne, "contenu", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, u"contenu", style(optionnel)).
    book = xlwt.Workbook(encoding='ascii')
    sheet = book.add_sheet(u"Rapports")
    rowx = 0
    sheet.write_merge(rowx, rowx + 1, 0, 3,\
                        u"Rapports de gestion de stock ULTIMO", style_title)

    rowx += 3
    sheet.write_merge(rowx, rowx, 1, 2, u"Date du rapport: ", style)
    date_com = "Bko le %s" % date.today().strftime("%d/%m/%Y")
    sheet.write_merge(rowx, rowx, 3, 3, date_com)

    sheet.col(1).width = 0x0d00 * 3
    sheet.col(2).width = 0x0d00 * 1.5
    sheet.col(4).width = 0x0d00 * 2
    hdngs = [u"Type", u"Produit", u"Nbre Carton", u"Restant", \
                                                                u"Date"]
    mag = ""
    for mag in session.query(Magasin).order_by(desc(Magasin.name)).all():
        rowx += 2
        sheet.write_merge(rowx, rowx, 0, 1, u"Magasin : " + mag.name, \
                                                                style_mag)
        rowx += 1
        for colx, value in enumerate(hdngs):
            sheet.write(rowx, colx, value, style_t_table)
        rowx += 1
        for rap in session.query(Rapport).filter(Rapport.magasin_id == mag.id):
            if int(rowx) % 2 == 0:
                style_row_table = style1
            else:
                style_row_table = style2
            sheet.write(rowx, 0, rap.type_, style_row_table)
            sheet.write(rowx, 1, rap.produit.libelle, style_row_table)
            sheet.write(rowx, 2, rap.nbr_carton, style_row_table)
            sheet.write(rowx, 3, rap.restant, style_row_table)
            sheet.write(rowx, 4, rap.date_rapp.strftime(u'%x %Hh:%Mmn'), \
                                                            style_row_table)
            rowx += 1
        sheet.write(rowx, 1, u"TOTAL", style_t_table)
        sheet.write(rowx, 2, u"", style_row_table)
        sheet.write(rowx, 3, "", style_row_table)

    book.save(file_name)
    return file_name


def write_xls_inventaire(rapport):
    pass
