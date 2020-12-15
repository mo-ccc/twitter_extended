import flask
from app import db

client = flask.Blueprint('client', __name__)

@client.cli.command('create')
def create_db():
    db.create_all()
    print("created all tables")
    
@client.cli.command('drop')
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("dropped all tables")