import pytest
from muffin.factories import create_app

import muffin.backend as backend


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
def db(request):
    pass
