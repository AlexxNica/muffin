# Copyright (C) Electronic Arts Inc.  All rights reserved.

from setuptools import setup
import muffin

setup(name='Muffin',
      version=muffin.VERSION,
      packages=['muffin', 'muffin/v2', 'muffin/manage'],
      py_modules=['wsgi', 'manage'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=[
          'flask',
          'jsonschema',
          'Flask-Script',
          'fake-factory',
          'jsonpatch',
          'Flask-SQLAlchemy'
      ]
      )
