# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
import flask
import muffin.backend as backend
from muffin.v2.request_utils import get_customer_id, create_reference_to

testsuites_blueprint = flask.Blueprint("testsuites", __name__)


@testsuites_blueprint.route('/testsuites', methods=['GET'])
def list_testsuites():
    customer_id = get_customer_id(flask.request)
    testsuites = []

    for suite in backend.get_testsuites(customer_id):
        testsuites.append(create_api_v2_testsuite(suite))

    return flask.jsonify({"testsuites": testsuites})


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['GET'])
def get_testsuite(testsuite_id):
    customer_id = get_customer_id(flask.request)

    suite = backend.get_testsuite(customer_id, testsuite_id)

    return flask.jsonify(create_api_v2_testsuite(suite))


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['DELETE'])
def delete_testsuite():
    return flask.jsonify({"hello": "world"})


def create_api_v2_testsuite(suite):
    return {
        'id' : suite['id'],
        'id_str' : str(suite['id']),
        'name' : suite['name'],
        'description' : suite['description'],
        'metadata' : json.loads(suite['metadata']),
        'references' : [create_reference_to('runs', 'testsuite_runs.list_testsuite_runs', suite=suite['id'])],
        'tags' : [] # TODO: implement tags
    }


def register_api(app, url_prefix):
    app.register_blueprint(testsuites_blueprint, url_prefix=url_prefix)
