#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, Column, Integer, String, \
                       MetaData, ForeignKey, Date, DateTime, Unicode

DB_FILE = 'gstock.db'

engine = create_engine('sqlite:///%s' % DB_FILE, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()


magasins_table = Table('magasin', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(20)),
    Column('adresse', Unicode(100)),
)

produits_table = Table('produit', metadata,
    Column('id', Integer, primary_key=True),
    Column('nbr_piece', Integer),
    Column('libelle', Unicode(100)),
)

rapports_table = Table('rapport', metadata,
    Column('id', Integer, primary_key=True),
    Column('magasin_id', Integer, ForeignKey('magasin.id')),
    Column('produit_id', Integer, ForeignKey('produit.id')),
    Column('nbr_carton', Integer),
    Column('restant', Integer),
    Column('date_rapp', DateTime),
    Column('registered_on', DateTime, nullable=True),
    Column('type_', Unicode(20)),
)

metadata.create_all(engine)


class Magasin(object):
    def __init__(self, name, adresse=""):
        self.name = name
        self.adresse = adresse

    def __repr__(self):
        return (u"Magasin (%(magasin)s %(adresse)s)") %\
                {'magasin': self.name, 'adresse': self.adresse}

    def __unicode__(self):
        return (u"%(magasin)s %(adresse)s") \
               % {'magasin': self.name, 'adresse': self.adresse}


class Produit(object):
    def __init__(self, libelle, nbr_piece):
        self.nbr_piece = nbr_piece
        self.libelle = libelle

    def __repr__(self):
        return (u"Produit(%(libelle)s %(nbr_piece)s)" % \
                                            {'libelle': self.libelle,\
                                            'nbr_piece': self.nbr_piece})

    def __unicode__(self):
        return (u"%(libelle)s %(nbr_piece)s" % {'libelle': self.libelle,\
                                              'nbr_piece': self.nbr_piece})


class Rapport(object):
    def __init__(self, type_, nbr_carton, date_rapp, remaining=0, \
                                        magasin=None, produit=None):
        self.type_ = type_
        self.magasin = magasin
        self.produit = produit
        self.nbr_carton = nbr_carton
        self.restant = remaining
        self.date_rapp = date_rapp
        self.registered_on = datetime.now()

    def __repr__(self):
        return ("Rapport('%(type_)s', '%(magasin)s', '%(produit)s', \
                '%(nbr_carton)s, '%(date_rapp)s')") % {'type_': self.type_, \
                'date_rapp': self.date_rapp, 'nbr_carton': self.nbr_carton, \
                'magasin': self.magasin, 'produit': self.produit}

    def __unicode__(self):
        return (u"%(type_)s %(date_rapp)s %(produit)s: %(magasin)s") \
               % {'type_': self.type_, \
                'date_rapp': self.date_rapp.strftime('%F'), \
                'produit': self.produit, 'magasin': self.magasin}


mapper(Produit, produits_table, properties={
    'rapports': relationship(Rapport, backref='produit'),
})
mapper(Magasin, magasins_table, properties={
    'rapports': relationship(Rapport, backref='magasin'),
    })
mapper(Rapport, rapports_table)
