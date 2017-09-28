# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
from muffin.v2.tests import get_json, create_customer_headers


def test_list_testsuites_all(app, backend, customer_id):
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "A test suite name",
                                 "description": "A description",
                                 "metadata": "{}"
                             })

    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "2nd testsuite",
                                 "description": "Foo bar",
                                 "metadata": str(json.dumps({"platform": "ps4"}))
                             })

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuites', headers=create_customer_headers(customer_id))

    assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuites']) == 2

    for ts in data['testsuites']:

        assert 'id' in ts
        assert 'id_str' in ts
        assert 'name' in ts
        assert 'description' in ts
        assert 'metadata' in ts

        assert 'references' in ts
        for ref in ts['references']:
            assert 'rel' in ref
            assert 'url' in ref
            if ref['rel'] == "runs":
                assert ref['url'] == '/api/v2/testsuiteruns?suite=' + str(ts['id'])

        assert 'tags' in ts
        # TODO : Verify tags


def test_list_testsuites_all_filter(app, backend, customer_id):
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "A test suite name",
                                 "description": "A description",
                                 "metadata": "{}"
                             })

    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "2nd testsuite",
                                 "description": "Foo bar",
                                 "metadata": str(json.dumps({"platform": "ps4"}))
                             })

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuites',
                              headers=create_customer_headers(customer_id),
                              query_string="fields=id,name,references")

    assert r.status_code == 200
    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuites']) == 2

    for ts in data['testsuites']:

        assert 'id' in ts
        assert 'name' in ts

        assert 'id_str' not in ts
        assert 'description' not in ts
        assert 'metadata' not in ts
        assert 'references' in ts
        assert 'tags' not in ts


def test_list_specific(app, backend, customer_id):
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "A test suite name",
                                 "description": "A description",
                                 "metadata": "{}"
                             })
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "2nd testsuite",
                                 "description": "Foo bar",
                                 "metadata": str(json.dumps({"platform": "ps4"}))
                             })

    # fetch and verify
    r = app.test_client().get('/api/v2/testsuites/1', headers=create_customer_headers(customer_id))

    assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    ts = get_json(r)

    assert 'id' in ts
    assert ts['id'] == 1

    assert 'id_str' in ts

    assert 'name' in ts
    assert ts['name'] == 'A test suite name'

    assert 'description' in ts
    assert 'metadata' in ts

    assert 'references' in ts
    for ref in ts['references']:
        assert 'rel' in ref
        assert 'url' in ref
        if ref['rel'] == "runs":
            assert ref['url'] == '/api/v2/testsuiteruns?suite=' + str(ts['id'])

    assert 'tags' in ts
    # TODO : Verify tags


def test_list_specific_fieldfilter(app, backend, customer_id):
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "A test suite name",
                                 "description": "A description",
                                 "metadata": "{}"
                             })
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "2nd testsuite",
                                 "description": "Foo bar",
                                 "metadata": str(json.dumps({"platform": "ps4"}))
                             })

    # filter to the id and foo fields, the foo field doesn't exist and should be ignored
    q = {"fields": ["id", "foo"]}
    r = app.test_client().get('/api/v2/testsuites/1', headers=create_customer_headers(customer_id), query_string=q)

    assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    ts = get_json(r)

    assert 'id' in ts
    assert ts['id'] == 1

    assert 'id_str' not in ts
    assert 'name' not in ts
    assert 'description' not in ts
    assert 'metadata' not in ts
    assert 'references' not in ts


def test_delete(app, backend, customer_id):
    backend.upsert_testsuite(customer_id,
                             {
                                 "name": "A test suite name",
                                 "description": "A description",
                                 "metadata": "{}"
                             })

    # fetch and verify
    r = app.test_client().delete('/api/v2/testsuites/5', headers=create_customer_headers(customer_id))

    assert r.status_code == 204

    assert 'X-ElapsedTime' in r.headers
