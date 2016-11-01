import flask

hello_blueprint = flask.Blueprint("hello", __name__)

@hello_blueprint.route('/')
def hello():
    return flask.jsonify({"hello": "world"})

def register_api(app, url_prefix):
    app.register_blueprint(hello_blueprint, url_prefix=url_prefix)
