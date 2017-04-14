# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask
import muffin.backend as backend

testsuites_blueprint = flask.Blueprint("testsuites", __name__)


@testsuites_blueprint.route('/testsuites', methods=['GET'])
def list_testsuites():
    testsuites = []

    backend.get_testsuites(None)
    return flask.jsonify({"testsuites": testsuites})


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['GET'])
def get_testsuite():
    return flask.jsonify({"hello": "world"})


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['DELETE'])
def delete_testsuite():
    return flask.jsonify({"hello": "world"})


def register_api(app, url_prefix):
    app.register_blueprint(testsuites_blueprint, url_prefix=url_prefix)
