import json
import flask
import muffin.muffin_error as muffin_error


def test_exception():
    try:
        raise muffin_error.MuffinError("A error happened", payload={"foo": "bar"}, status_code=500)
    except muffin_error.MuffinError as e:
        assert e.message == "A error happened"
        assert e.payload == {"foo": "bar"}
        assert e.status_code == 500


def test_exception_dict():
    try:
        raise muffin_error.MuffinError("A error happened", payload={"foo": "bar"}, status_code=500)
    except muffin_error.MuffinError as e:
        d = e.to_dict()
        assert 'message' in d
        assert d['message'] == 'A error happened'
        assert 'foo' in d
        assert d['foo'] == "bar"
        assert 'statusCode' in d
        assert d['statusCode'] == 500


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def test_muffin_error(app):
    @app.route("/raise")
    def fail():
        raise muffin_error.MuffinError("Useful error message", status_code=418)

    r = app.test_client().get('/raise')
    assert r.status_code == 418

    data = get_json(r)
    assert 'statusCode' in data
    assert data['statusCode'] == 418
    assert 'message' in data
    assert 'stackTrace' in data

    del fail


def test_400(app):
    @app.route("/raise")
    def fail():
        flask.abort(400)

    r = app.test_client().get('/raise')
    assert r.status_code == 400

    data = get_json(r)
    assert 'statusCode' in data
    assert data['statusCode'] == 400
    assert 'message' in data

    del fail


def test_404(app):
    r = app.test_client().get('/foo')
    assert r.status_code == 404

    data = get_json(r)
    assert 'statusCode' in data
    assert data['statusCode'] == 404
    assert 'message' in data


def test_500(app):
    @app.route("/raise")
    def fail():
        flask.abort(500)

    r = app.test_client().get('/raise')
    assert r.status_code == 500

    data = get_json(r)
    assert 'statusCode' in data
    assert data['statusCode'] == 500
    assert 'message' in data
    assert 'stackTrace' in data

    del fail
