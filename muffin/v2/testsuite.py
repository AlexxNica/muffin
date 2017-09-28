# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
import flask
import muffin.backend as backend
from muffin.v2.request_utils import (get_customer_id, create_reference_to, get_common_params,
                                     apply_mapping_to_db_fields, map_db_record_to_dict)

testsuites_blueprint = flask.Blueprint("testsuites", __name__)


def to_db_columns(fields):
    mapping = {"id": "id", "id_str": 'id', "name": "name", "metadata": "metadata", "description": "description",
               "references": ["id"]}

    return apply_mapping_to_db_fields(fields, mapping)


def create_api_v2_testsuite(fields, suite):
    mapping = {"id": "", "id_str": lambda s: s["id"], "name": "", "description": "",
               "metadata": lambda s: json.loads(s["metadata"]),
               "references": lambda s: [
                   create_reference_to('runs', 'testsuite_runs.list_testsuite_runs', suite=s['id'])
                   ],
               "tags": ""}

    record = map_db_record_to_dict(suite, mapping, fields)

    if not fields or "tags" in fields:
        record["tags"] = []  # TODO: implement tags
    return record


@testsuites_blueprint.route('/testsuites', methods=['GET'])
def list_testsuites():
    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)

    testsuites = []

    db_fields = to_db_columns(fields)
    for suite in backend.get_testsuites(customer_id, db_fields):
        testsuites.append(create_api_v2_testsuite(fields, suite))

    return flask.jsonify({"testsuites": testsuites})


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['GET'])
def get_testsuite(testsuite_id):
    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)

    db_fields = to_db_columns(fields)
    suite = backend.get_testsuite(customer_id, testsuite_id, db_fields)

    return flask.jsonify(create_api_v2_testsuite(fields, suite))


@testsuites_blueprint.route('/testsuites/<int:testsuite_id>', methods=['DELETE'])
def delete_testsuite(testsuite_id):  # pylint:disable=W0613
    # TODO: Implement DELETE of Testsuite
    return "", 204


def register_api(app, url_prefix):
    app.register_blueprint(testsuites_blueprint, url_prefix=url_prefix)
