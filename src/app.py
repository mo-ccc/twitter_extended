import flask

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()


def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("default_settings.py")
    
    
    db.init_app(app)
    
    from commands import client
    app.register_blueprint(client)
    
    from controllers import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)
    
    return app