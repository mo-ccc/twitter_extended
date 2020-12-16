import flask
import flask_jwt_extended
from app import db
from models.User import User
from models.Tweet import Tweet
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

admins = flask.Blueprint("admins", __name__)

@admins.route('/admin', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_admin_page():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user or not user.is_admin:
        return flask.abort(404)
    
    average_tweets_per_user = db.engine.execute(
        """
        SELECT AVG(count) FROM
        (SELECT users.id, COUNT(tweets.author_id)
        FROM tweets
        INNER JOIN users ON tweets.author_id = users.id
        GROUP BY users.id) congregate;
        """
    ).fetchone()[0]
    
    most_tweets_by_one_user = db.engine.execute(
        """
        select id, MAX(count) mx FROM
        (SELECT users.id, COUNT(tweets.author_id)
        FROM tweets
        INNER JOIN users ON tweets.author_id = users.id
        GROUP BY users.id) congregate
        GROUP BY id
        ORDER BY mx DESC LIMIT 1;
        """
    ).fetchone()
    user_with_max_tweets = User.query.get(most_tweets_by_one_user[0])
    max_tweets = most_tweets_by_one_user[1]
    
    return flask.render_template('admin.html', auth=jwt_id, avg=average_tweets_per_user,
        max_user=user_with_max_tweets, mx=max_tweets)
        
@admins.route('/admin/dump', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_dump():
    import os
    dump = os.popen("pg_dump --dbname=postgres://postgres:postgres@localhost:5432/postgres").read()
    return flask.Response(
        dump, headers={"Content-Disposition":"attachment;filename=dump.psql"}
    )
    