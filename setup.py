# Copyright (C) Electronic Arts Inc.  All rights reserved.
"""
Muffin
-----
Muffin is a web service and a REST API for structured test result reporting.

Links
`````
* `documentation <https://electronicarts.github.io/muffin>`_
* `github <https://github.com/electronicarts/muffin>`_
"""

from setuptools import setup
import muffin

setup(
    name='MuffinService',
    version=muffin.VERSION,
    description="Muffin is a solution for structured test result reporting",
    long_description=__doc__,
    packages=['muffin', 'muffin/v2', 'muffin/manage'],
    py_modules=['manage'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5'],
    install_requires=[
        'Flask',
        'jsonschema',
        'Flask-Script',
        'fake-factory',
        'jsonpatch',
        'Flask-SQLAlchemy',
        'python-dateutil']
    )
