import flask

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

import flask_jwt_extended
jwt = flask_jwt_extended.JWTManager()

import flask_marshmallow
ma = flask_marshmallow.Marshmallow()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("default_settings.py")
    
    
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(ma)
    
    from commands import client
    app.register_blueprint(client)
    
    from controllers import blueprints as controller_blueprints
    for bp in controller_blueprints:
        app.register_blueprint(bp)
    
    return app