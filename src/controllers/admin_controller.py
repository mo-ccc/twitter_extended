import flask
import flask_jwt_extended
from app import db
from models.User import User

admins = flask.Blueprint("admins", __name__)

@admins.route('/admin', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_admin_page():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user or not user.is_admin:
        return flask.abort(404)
    
    return flask.render_template('admin.html', auth=jwt_id)