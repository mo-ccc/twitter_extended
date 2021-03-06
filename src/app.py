import flask

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

import flask_jwt_extended
jwt = flask_jwt_extended.JWTManager()

@jwt.expired_token_loader
def my_expired_token_callback():
    return flask.redirect("/logout", code=302)

import flask_bcrypt
bcrypt = flask_bcrypt.Bcrypt()

import flask_marshmallow
ma = flask_marshmallow.Marshmallow()

import flask_migrate
migrate = flask_migrate.Migrate()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_object("default_settings.configuration")
    
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    from commands import db_cli
    app.register_blueprint(db_cli)
    
    from controllers import blueprints as controller_blueprints
    for bp in controller_blueprints:
        app.register_blueprint(bp)
    
    return app