# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask


ping_blueprint = flask.Blueprint("ping", __name__)


@ping_blueprint.route('/ping')
def ping():  # pragma: no cover
    return flask.jsonify({"hello": "world"})


def register_api(app, url_prefix):
    app.register_blueprint(ping_blueprint, url_prefix=url_prefix)

    from . import testsuite
    from . import testsuite_runs

    testsuite.register_api(app, url_prefix)
    testsuite_runs.register_api(app, url_prefix)
