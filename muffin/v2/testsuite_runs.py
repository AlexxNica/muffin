# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask
#import muffin.backend as backend
#from muffin.v2.request_utils import get_customer_id, create_reference_to

testsuite_runs_blueprint = flask.Blueprint("testsuite_runs", __name__)


@testsuite_runs_blueprint.route('/testsuiteruns', methods=['GET'])
def list_testsuite_runs():  # pragma: no cover

    #customer_id = get_customer_id(flask.request)
    runs = []

    # TODO : implement
    return flask.jsonify({"testsuiteruns": runs})

def register_api(app, url_prefix):
    app.register_blueprint(testsuite_runs_blueprint, url_prefix=url_prefix)
