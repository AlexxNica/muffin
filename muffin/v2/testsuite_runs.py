# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
from datetime import datetime
import flask
import muffin.backend as backend
from muffin.v2.request_utils import (get_customer_id, get_common_params, create_reference_to,
                                     apply_mapping_to_db_fields, map_db_record_to_dict)
from muffin.muffin_error import MissingFieldsError
import dateutil.parser

testsuite_runs_blueprint = flask.Blueprint("testsuite_runs", __name__)


def create_api_v2_testsuiterun(fields, run):
    mapping = {"id": "", "id_str": lambda s: str(s["id"]), "createdAt": "", "startedAt": "",
               "endedAt": "", "state": "", "result": "",
               "metadata": lambda s: json.loads(s["metadata"]),
               "references": lambda s: [
                   create_reference_to('runs', 'testsuite_runs.list_testsuite_runs', suite=s['id'])
                   ]}

    record = map_db_record_to_dict(run, mapping, fields)

    if not fields or "tags" in fields:
        record["tags"] = []  # TODO: implement tags
    return record


def to_db_columns(fields):
    mapping = {"id": "id", "id_str": 'id', "createdAt": "createdAt", "startedAt": "startedAt",
               "endedAt": "endedAt", "state": "state", "result": "result",
               "metadata": "metadata",
               "references": ["id"]}

    return apply_mapping_to_db_fields(fields, mapping)


@testsuite_runs_blueprint.route('/testsuiteruns', methods=['GET'])
def list_testsuite_runs():

    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)
    db_fields = to_db_columns(fields)

    runs = backend.get_testsuite_runs(customer_id, db_fields)
    # TODO : implement pagination
    return flask.jsonify({"testsuiteruns": [create_api_v2_testsuiterun(fields, r) for r in runs]})


@testsuite_runs_blueprint.route('/testsuiteruns/<int:run_id>', methods=['GET'])
def list_testsuite_run(run_id):

    customer_id = get_customer_id(flask.request)
    (fields, _) = get_common_params(flask.request)
    db_fields = to_db_columns(fields)

    run = backend.get_testsuite_run(customer_id, run_id, db_fields)
    return flask.jsonify({"testsuiteruns": [create_api_v2_testsuiterun(fields, run)]})


@testsuite_runs_blueprint.route('/testsuiteruns', methods=['POST'])
def post_testsuite_runs():
    content = flask.request.get_json(force=True)
    customer_id = get_customer_id(flask.request)

    missing_fields = []
    if 'name' not in content:
        missing_fields.append('name')
    if 'description' not in content:
        missing_fields.append('description')

    # if one of the two fields that indicate a finished run is present, both fields must be present
    if 'endedAt' in content and 'result' not in content:
        missing_fields.append('result')
    if 'result' in content and 'endedAt' not in content:
        missing_fields.append('endedAt')

    if missing_fields:
        raise MissingFieldsError(missing_fields)

    testsuite = {
        'name': content['name'],
        'description': content['description'],
        }
    testsuite_id = backend.upsert_testsuite(customer_id, testsuite)

    testsuite_run = {
        "metadata": content.get("metadata", ""),
        "createdAt": datetime.now()
    }

    started = None
    ended = None
    if "startedAt" in content:
        started = {
            "startedAt": dateutil.parser.parse(content["startedAt"])
        }
    if "endedAt" in content:
        ended = {
            "endedAt": dateutil.parser.parse(content["endedAt"]),
            "result": content["result"]
        }

    new_id = backend.insert_testsuite_run(customer_id, testsuite_id, testsuite_run, started, ended)

    # TODO: Tags are not implemented
    return flask.jsonify({"id": new_id, "id_str": str(new_id)})


def register_api(app, url_prefix):
    app.register_blueprint(testsuite_runs_blueprint, url_prefix=url_prefix)
