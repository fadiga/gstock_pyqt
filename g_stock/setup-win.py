#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import os

from distutils.core import setup
import py2exe

try:
    target = os.environ['PY2EXE_MODE']
except KeyError:
    target = 'multi'

if target == 'single':
    ZIPFILE = None
    BUNDLES = 1
else:
    ZIPFILE = 'shared.lib'
    BUNDLES = 1

setup(windows=[{'script': 'gmag.py', \
                'icon_resources': [(0, 'images\\ap.ico')]}],
      options={'py2exe': {
                    'includes': ['sip'],
                    'packages': ['sqlalchemy.dialects.sqlite'],
                    'compressed': True,
                    'bundle_files': BUNDLES,
                    },
               },
      zipfile=ZIPFILE,
)
