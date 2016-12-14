[![Build Status](https://travis-ci.org/patissiere/muffin.svg?branch=master)](https://travis-ci.org/patissiere/muffin)
[![Code Health](https://landscape.io/github/patissiere/muffin/master/landscape.svg?style=flat)](https://landscape.io/github/patissiere/muffin/master)
[![codecov](https://codecov.io/gh/patissiere/muffin/branch/master/graph/badge.svg)](https://codecov.io/gh/patissiere/muffin)
[![docs](https://img.shields.io/badge/docs-Read-blue.svg)](https://patissiere.github.io/muffin/)
[![PyPI](https://img.shields.io/pypi/v/MuffinService.svg)](https://pypi.python.org/pypi/MuffinService)

# Muffin
Muffin is a structured reporting solution for test results

# Setting up dev environment
Install [Python3](https://www.python.org/downloads/) (preferrably Python 3.5).

Install dependencies by running (preferrably in a [virtualenv](https://virtualenv.pypa.io/en/latest/))

	$ pip install -r requirements.txt

Use the example config in `muffin/muffin.cfg.sample` and rename it to `muffin/muffin.cfg`.

Now you should be good to go by running

	$ python manage.py runserver

in the top-level folder.

# Tests
Run

	$ py.test

in the root directory to run all the tests.

# Contributing

- Make sure you document any API changes
- Update the changelog
- All new functionality must have unit tests
- Unit tests coverage must be 100% at all times. Exclude things that should not be part of coverage statistics.

# API Spec

- Each endpoint should be clearly documented in which fields it supports filtering on, 
pass the query to filter as a json object in the filter argument.
- Each endpoint should support selecting which fields to return using a 
comma separated fields attribute
- Never return naked arrays as the top level object, return the pluralized form of 
the resource you are working on.
- Patch endpoints accept json patch objects or return 403 if run on a 
field / the operation is not allowed
- JSON output is camelCased.
- PUT, POST and PATCH responses return a location header to the created / modified 
(using 201 header in that case) object and the id to that object.
- When a piece of data exists independently of others, use a top level endpoint, otherwise use 
a nested route (such as /testsuiteruns/1/comments). 
- When returning a piece of data through a relationship, return an alias to retrieve the entire 
relationship. If its a one-to-one relationship use the actual endpoint.
- Frosting API is always paginated by using the 5988 RFC and the Page, Per Page query parameter.
- Frosting endpoints are always in plural.
- Every response comes with a X-ElapsedTime header declaring how long it took to serve that command

Unless otherwise stated above follow the guidelines specified here:
http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
