#!/usr/bin/env python
# encoding= utf-8
#maintainer : Fad

from datetime import datetime
from database import *


m = Magasin(u"Bozola n1")
m1 = Magasin(u"Razel")
p = Produit(u"Roulements", 250)
p1 = Produit(u"piston", 10)
p2 = Produit(u"pause pied", 20)

rap = Rapport(u"Entre", 30, datetime(2011, 02, 01, 18, 20, 22, 88), 50)
rap.magasin = m
rap.produit = p
rap1 = Rapport(u"Entre", 10, datetime(2011, 05, 01, 04, 10, 12, 88), 50)
rap1.magasin = m1
rap1.produit = p1

rap2 = Rapport(u"Entre", 150, datetime(2011, 03, 01, 18, 20, 22, 88), 50)
rap2.magasin = m1
rap2.produit = p2

try:
    print "Enregistrement ..."
    session.add_all((m, m1, p, p2, rap, rap1, rap2))
    print "commit ..."
    session.commit()
    print "Ok"
    print "Les produit"
    for pro in session.query(Produit).all():
        print pro
    print "Les rapport"
    for rap in session.query(Rapport).all():
        print rap
except:
    session.rollback()
    print "Ereur !!!"
