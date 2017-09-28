# Copyright (C) Electronic Arts Inc.  All rights reserved.

from datetime import datetime
import flask
import muffin.backend as backend
from muffin.v2.request_utils import get_customer_id
from muffin.muffin_error import MissingFieldsError
import dateutil.parser

testsuite_runs_blueprint = flask.Blueprint("testsuite_runs", __name__)


@testsuite_runs_blueprint.route('/testsuiteruns', methods=['GET'])
def list_testsuite_runs():  # pragma: no cover

    # customer_id = get_customer_id(flask.request)
    runs = []

    # TODO : implement
    return flask.jsonify({"testsuiteruns": runs})



@testsuite_runs_blueprint.route('/testsuiteruns', methods=['POST'])
def post_testsuite_runs():
    content = flask.request.get_json(force=True)
    customer_id = get_customer_id(flask.request)

    missing_fields = []
    if not 'name' in content:
        missing_fields.append('name')
    if not 'description' in content:
        missing_fields.append('description')

    # if one of the two fields that indicate a finished run is present, both fields must be present
    if 'endedAt' in content and not 'result' in content:
        missing_fields.append('result')
    if 'result' in content and not 'endedAt' in content:
        missing_fields.append('endedAt')

    if missing_fields:
        raise MissingFieldsError(missing_fields)

    testsuite = {
        'name' : content['name'],
        'description' : content['description'],
        }
    testsuite_id = backend.upsert_testsuite(customer_id, testsuite)

    testsuite_run = {
        "metadata" : content.get("metadata", ""),
        "createdAt" : datetime.now()
    }

    started = None
    ended = None
    if "startedAt" in content:
        started = {
            "startedAt" : dateutil.parser.parse(content["startedAt"])
        }
    if "endedAt" in content:
        ended = {
            "endedAt" : dateutil.parser.parse(content["endedAt"]),
            "result": content["result"]
        }

    new_id = backend.insert_testsuite_run(customer_id, testsuite_id, testsuite_run, started, ended)

    # TODO: Tags are not implemented
    return flask.jsonify({"id": new_id, "id_str": str(new_id)})


def register_api(app, url_prefix):
    app.register_blueprint(testsuite_runs_blueprint, url_prefix=url_prefix)
