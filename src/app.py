import flask

import flask_sqlalchemy
db = flask_sqlalchemy.Sqlalchemy()


def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("default_settings")
    db.init_app(app)
    return app