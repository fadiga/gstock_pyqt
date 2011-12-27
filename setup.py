#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='gstock',
    version = "V.0.1",
    license='GNU Lesser General Public License (LGPL), Version 3',

    install_requires=['SQLAlchemy>=0.6.6','pysqlite'],
    provides=['gstock'],
	autor = "Fadiga",
    description='Gestion des magasin de stock G.U.I',
    long_description=open('README.rst').read(),

    url='http://github.com/yeleman/anm',

    packages=['gstock'],

    classifiers=[
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
)
