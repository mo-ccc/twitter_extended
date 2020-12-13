import flask

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

import flask_jwt_extended
jwt = flask_jwt_extended.JWTManager()
@jwt.expired_token_loader
def my_expired_token_callback():
    return flask.redirect("http://127.0.0.1:5000/login", code=302)

import flask_bcrypt
bcrypt = flask_bcrypt.Bcrypt()

import flask_marshmallow
ma = flask_marshmallow.Marshmallow()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("default_settings.py")
    
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    
    from commands import client
    app.register_blueprint(client)
    
    from controllers import blueprints as controller_blueprints
    for bp in controller_blueprints:
        app.register_blueprint(bp)
    
    return app