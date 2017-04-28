# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
import flask
import muffin.backend as backend
from muffin.v2.request_utils import get_customer_id, create_reference_to, get_common_params

testsuites_blueprint = flask.Blueprint("testsuites", __name__)


def _fields_to_db_columns(fields):
    if not fields:
        return None

    mapping = {"id": "id", "id_str": 'id', "name": "name", "metadata": "metadata", "description": "description",
               "references": ["id"]}

    db_fields = []
    for f in fields:
        x = mapping[f]
        if isinstance(x, list):
            db_fields.extend(x)
        else:
            db_fields.append(x)
    return db_fields


@testsuites_blueprint.route('/testsuites', methods=['GET'])
def list_testsuites():
    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)

    testsuites = []

    db_fields = _fields_to_db_columns(fields)
    for suite in backend.get_testsuites(customer_id, db_fields):
        testsuites.append(create_api_v2_testsuite(fields, suite))

    return flask.jsonify({"testsuites": testsuites})


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['GET'])
def get_testsuite(testsuite_id):
    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)

    db_fields = _fields_to_db_columns(fields)
    suite = backend.get_testsuite(customer_id, testsuite_id, db_fields)

    return flask.jsonify(create_api_v2_testsuite(fields, suite))


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['DELETE'])
def delete_testsuite(testsuite_id):  # pylint:disable=W0613
    # TODO: Implement DELETE of Testsuite
    return "", 204


def create_api_v2_testsuite(fields, suite):
    d = {}
    all_fields = fields is None
    if all_fields or "id" in fields:
        d["id"] = suite['id']
    if all_fields or "id_str" in fields:
        d["id_str"] = str(suite['id'])
    if all_fields or "name" in fields:
        d["name"] = suite['name']
    if all_fields or "description" in fields:
        d["description"] = suite['description']
    if all_fields or "metadata" in fields:
        d["metadata"] = json.loads(suite['metadata'])
    if all_fields or "references" in fields:
        d["references"] = [create_reference_to('runs', 'testsuite_runs.list_testsuite_runs', suite=suite['id'])]
    if all_fields or "tags" in fields:
        d["tags"] = []  # TODO: implement tags

    return d


def register_api(app, url_prefix):
    app.register_blueprint(testsuites_blueprint, url_prefix=url_prefix)
