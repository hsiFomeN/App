import flask
from flask import make_response, jsonify

from data import db_session
from theses import Theses

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@blueprint.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@blueprint.route('/api/theses')
def get_news():
    db_sess = db_session.create_session()
    thesis = db_sess.query(Theses).all()
    return jsonify(
        {
            'theses':
                [item.to_dict(only=('title', 'thesis_filename', 'user.name', 'user.surname', 'user.organisation'))
                 for item in thesis]
        }
    )


@blueprint.route('/api/theses/<int:theses_id>', methods=['GET'])
def get_one_news(theses_id):
    db_sess = db_session.create_session()
    thesis = db_sess.query(Theses).get(theses_id)
    if not thesis:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': thesis.to_dict(only=(
                'title', 'thesis_filename', 'user_id'))
        }
    )