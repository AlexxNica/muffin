# Copyright (C) Electronic Arts Inc.  All rights reserved.

from datetime import datetime
import json
from muffin.v2.tests import get_json, create_customer_headers


def test_list_testsuitesruns(app, backend, customer_id):
    testsuite = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}"}

    testsuite_id = backend.upsert_testsuite(customer_id, testsuite)

    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": "{}",
                                     "createdAt": datetime.now(),
                                 },
                                 {
                                     "startedAt": datetime.now(),
                                 })

    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": str(json.dumps({"foo": "bar"})),
                                     "createdAt": datetime.now(),
                                 },
                                 {
                                     "startedAt": datetime.now(),
                                 },
                                 {
                                     "endedAt": datetime.now(),
                                     "result": 0  # successful
                                 })

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuiteruns', headers=create_customer_headers(customer_id))

    # TODO: Not implemented
    # assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuiteruns']) == 2
    # TODO: Check for pagination


def test_list_testsuitesruns_fieldfilter(app, backend, customer_id):
    testsuite = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}"}

    testsuite_id = backend.upsert_testsuite(customer_id, testsuite)

    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": "{}",
                                     "createdAt": datetime.now(),
                                 },
                                 {
                                     "startedAt": datetime.now(),
                                 })

    backend.insert_testsuite_run(customer_id, testsuite_id,
                                 {
                                     "testsuite": testsuite_id,
                                     "metadata": str(json.dumps({"foo": "bar"})),
                                     "createdAt": datetime.now(),
                                 },
                                 {
                                     "startedAt": datetime.now(),
                                 },
                                 {
                                     "endedAt": datetime.now(),
                                     "result": 0  # successful
                                 })

    # filter to the id and description fields, the description field doesn't exist and should be ignored
    q = {"fields": ["id", "description"]}
    r = app.test_client().get('/api/v2/testsuiteruns', headers=create_customer_headers(customer_id), query_string=q)

    # TODO: Not implemented
    # assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuiteruns']) == 2
    for r in data['testsuiteruns']:
        assert 'id' in r
        assert 'metadata' not in r

    # TODO: Check for pagination


def test_list_testsuitesrun(app, backend, customer_id):
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
                                 })

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
                                     "result": 0  # successful
                                 })

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuiteruns/2', headers=create_customer_headers(customer_id))

    assert r.status_code == 200
    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuiteruns']) == 1
    run = data['testsuiteruns'][0]
    assert run
    assert 'id' in run
    assert run['id'] == 2
    assert 'id_str' in run
    assert run['id_str'] == '2'
    assert 'createdAt' in run
    # TODO: Event sourcing lookups needsed in the backend
    # assert 'startedAt' in run
    # assert 'state' in run
    assert 'metadata' in run


def test_list_testsuitesrun_fieldfilter(app, backend, customer_id):
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
                                 })

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
                                     "result": 0  # successful
                                 })

    # filter to the id and description fields, the description field doesn't exist and should be ignored
    q = {"fields": ["id", "description"]}
    r = app.test_client().get('/api/v2/testsuiteruns/2', headers=create_customer_headers(customer_id), query_string=q)

    assert r.status_code == 200
    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuiteruns']) == 1
    run = data['testsuiteruns'][0]
    assert run
    assert 'id' in run
    assert run['id'] == 2
    assert 'id_str' not in run
    assert 'createdAt' not in run
    assert 'startedAt' not in run
    assert 'state' not in run
    assert 'metadata' not in run


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


def test_post_testsuiterun_complete(app, backend, customer_id):
    """
    Verifies that the post endpoint can accept a already finished run of a test suite complete with result
    """
    run = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}",
        "startedAt": str(datetime.now()),
        "endedAt": str(datetime.now()),
        "result": "succeeded"  # succeeded
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


def test_post_testsuiterun_missing_field(app, customer_id):
    """
    Verifies that the post endpoint correctly reports which fields are missing for partial queries
    """

    run = {
        # name is missing
        # description is also missing
        "metadata": "{}",
    }

    r = app.test_client().post('/api/v2/testsuiteruns', data=json.dumps(run),
                               headers=create_customer_headers(customer_id))

    data = get_json(r)
    assert r.status_code == 400
    assert 'X-ElapsedTime' in r.headers

    assert 'message' in data
    assert 'fields' in data
    f = data["fields"]
    assert "name" in f
    assert 'description' in f


def test_post_testsuiterun_missing_field_result(app, customer_id):
    """
    Verifies that the post endpoint correctly reports which fields are missing for partial queries
    """

    run = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}",
        "endedAt": str(datetime.now()),
        # result is missing
    }

    r = app.test_client().post('/api/v2/testsuiteruns', data=json.dumps(run),
                               headers=create_customer_headers(customer_id))

    data = get_json(r)
    assert r.status_code == 400
    assert 'X-ElapsedTime' in r.headers

    assert 'message' in data
    assert 'fields' in data
    f = data["fields"]
    assert "result" in f


def test_post_testsuiterun_missing_field_endedAt(app, customer_id):
    """
    Verifies that the post endpoint correctly reports which fields are missing for partial queries
    """

    run = {
        "name": "A test suite name",
        "description": "A description",
        "metadata": "{}",
        "result": "failure",
        # endedAt is missing
        }

    r = app.test_client().post('/api/v2/testsuiteruns', data=json.dumps(run),
                               headers=create_customer_headers(customer_id))

    data = get_json(r)
    assert r.status_code == 400
    assert 'X-ElapsedTime' in r.headers

    assert 'message' in data
    assert 'fields' in data
    f = data["fields"]
    assert "endedAt" in f
