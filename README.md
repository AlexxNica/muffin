[![Build Status](https://travis-ci.org/electronicarts/muffin.svg?branch=master)](https://travis-ci.org/electronicarts/muffin)
[![Code Health](https://landscape.io/github/electronicarts/muffin/master/landscape.svg?style=flat)](https://landscape.io/github/electronicarts/muffin/master)
[![codecov](https://codecov.io/gh/electronicarts/muffin/branch/master/graph/badge.svg)](https://codecov.io/gh/electronicarts/muffin)
[![docs](https://img.shields.io/badge/docs-Read-blue.svg)](https://electronicarts.github.io/muffin/)
[![PyPI](https://img.shields.io/pypi/v/MuffinService.svg)](https://pypi.python.org/pypi/MuffinService)

# Muffin
Muffin is a structured reporting solution for test results

# Setting up dev environment
Install [Python3](https://www.python.org/downloads/) (preferrably Python 3.6).

Install dependencies by running (preferrably in a [virtualenv](https://virtualenv.pypa.io/en/latest/))

`$ pip install -r requirements.txt`

Use the example config in `muffin/muffin.cfg.sample` and rename it to `muffin/muffin.cfg`.

Now you should be good to go by running

`$ python manage.py runserver`

in the top-level folder.

# Tests
Run

`$ py.test`

in the root directory to run all the tests.

# API Spec
The rendered API documentation is available [here](https://electronicarts.github.io/muffin/api/), while the documentation 
source is available in the [source tree](docs) in the [Swagger](http://swagger.io/) specification.

When contributing API changes, please follow the [API Guidelines](api_guidelines.md).
