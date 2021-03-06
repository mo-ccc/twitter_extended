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
    
    # query will return the average number of tweets per user
    average_tweets_per_user = db.engine.execute(
        """
        SELECT AVG(count) FROM
        (SELECT users.id, COUNT(tweets.author_id)
        FROM tweets
        INNER JOIN users ON tweets.author_id = users.id
        GROUP BY users.id) congregate;
        """
    ).fetchone()[0]
    
    # query will get the user with the most tweets and the number of tweets they made
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
        
@admins.route('/admin/backup', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_backup():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user or not user.is_admin:
        return flask.abort(404)

    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # bash script to run pg_dump on the db
    dump = os.popen(f"pg_dump --dbname=postgres://{os.getenv('DB_URI')}").read()
    return flask.Response(
        dump, headers={"Content-Disposition":"attachment;filename=dump.psql"}
    )

@admins.route('/admin/dump', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_dump():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user or not user.is_admin:
        return flask.abort(404)
    
    # a very big query to get all data from all the tables in the database
    dump = db.engine.execute("""
        select * from users
        left join accounts on 1=1
        left join tweets on 1=1
        left join emotes on 1=1
        left join favourite_emotes on 1=1
        left join tweet_emote_joint on 1=1;
    """).fetchall()
    return str(dump)
    