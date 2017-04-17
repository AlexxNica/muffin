# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
from muffin.v2.tests import get_json, create_customer_headers

def test_list(app, backend, customer_id):
    backend.insert_testsuites([
        {
            "name": "A test suite name",
            "description": "A description",
            "metadata": "{}"
        },
        {
            "name": "2nd testsuite",
            "description": "Foo bar",
            "metadata": str(json.dumps({"platform": "ps4"}))
        }
    ])

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


def test_list_specific(app, backend, customer_id):
    backend.insert_testsuites([
        {
            "id" : 1,
            "name": "A test suite name",
            "description": "A description",
            "metadata": "{}"
        },
        {
            "id" : 2,
            "name": "2nd testsuite",
            "description": "Foo bar",
            "metadata": str(json.dumps({"platform": "ps4"}))
        }
    ])

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
