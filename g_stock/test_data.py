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

rap = Rapport(u"Entre", 50, datetime(2011, 02, 01, 18, 20,22,88), 50)
rap.magasin = m
rap.produit = p

try:
    print "Enregistrement ..."
    session.add_all((m, m1, p, p2, rap))
    print "commit ..."
    session.commit()
    print "Ok"
    print "Les produit"
    for pro in session.query(Produit).all(): print pro
    print "Les rapport"
    for rap in session.query(Rapport).all(): print rap
except:
    session.rollback()
    print "Ereur !!!"
