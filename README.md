[![Build Status](https://travis-ci.org/patissiere/muffin.svg?branch=master)](https://travis-ci.org/patissiere/muffin)

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
