# Copyright (C) Electronic Arts Inc.  All rights reserved.

import pytest
from muffin.factories import create_app

import muffin.backend as backend  # pylint: disable=unused-import


@pytest.fixture()
def app(request):
    application = create_app('muffin.testing.cfg')
    application.config['TESTING'] = True

    ctx = application.app_context()
    ctx.push()

    def finalize():
        ctx.pop()

    request.addfinalizer(finalize)

    return application


@pytest.fixture()
def db(request):  # pylint: disable=unused-argument
    pass
