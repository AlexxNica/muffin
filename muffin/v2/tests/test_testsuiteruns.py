# Copyright (C) Electronic Arts Inc.  All rights reserved.

from datetime import datetime
import json
from muffin.v2.tests import get_json, create_customer_headers


def test_list_testsuitesruns(app, backend, customer_id):
    testsuite = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}"
    }

    testsuite_id = backend.upsert_testsuite(customer_id, testsuite)

    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": "{}"
                                 },
                                 {
                                     "createdAt": datetime.now(),
                                 }
                                )
    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": str(json.dumps({"foo": "bar"}))
                                 },
                                 {
                                     "createdAt": datetime.now(),
                                 },
                                 {
                                     "endedAt": datetime.now(),
                                     "result": 0 # succesful
                                 },
                                )

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuiteruns', headers=create_customer_headers(customer_id))

    assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuiteruns']) == 2


def test_post_testsuiterun(app, backend, customer_id):
    run = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}"
    }

    r = app.test_client().post('/api/v2/testsuiteruns', data=json.dumps(run),
                               headers=create_customer_headers(customer_id))

    data = get_json(r)
    assert r.status_code == 200
    assert 'X-ElapsedTime' in r.headers

    assert 'id' in data
    assert 'id_str' in data

    i = data["id"]
    assert i == 1
    db_run = backend.get_testsuite_run(customer_id, i, None)
    assert db_run
