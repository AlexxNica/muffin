# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json
from muffin.v2.tests import get_json

def test_list(app, backend):
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
    r = app.test_client().get('/api/v2/testsuites')

    assert r.status_code == 200

    assert 'X-ElapsedTime' in r.headers

    data = get_json(r)
    assert len(data['testsuites']) == 2

    for ts in data['testsuites']:

        assert 'name' in ts
        assert 'description' in ts
        assert 'metadata' in ts

        assert 'references' in ts
        for ref in ts['references']:
            assert 'rel' in ref
            assert 'url' in ref
            if ref['rel'] == "runs":
                assert ref['runs'] == '/api/v2/testsuiteruns?suite=' + str(ts['id'])
