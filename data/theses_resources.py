from data import db_session
from data.theses import Theses
from flask_restful import Resource, reqparse
from flask import abort, jsonify


def abort_if_theses_not_found(theses_id):
    session = db_session.create_session()
    theses = session.query(Theses).get(theses_id)
    if not theses:
        abort(404, message=f"Theses {theses_id} not found")


class ThesesResource(Resource):
    def get(self, theses_id):
        abort_if_theses_not_found(theses_id)
        session = db_session.create_session()
        theses = session.query(Theses).get(theses_id)
        return jsonify({'theses': theses.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, theses_id):
        abort_if_theses_not_found(theses_id)
        session = db_session.create_session()
        theses = session.query(Theses).get(theses_id)
        session.delete(theses)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


class ThesesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        theses = session.query(Theses).all()
        return jsonify({'theses': [item.to_dict(
            only=('title', 'thesis_filename', 'user.name', 'user.surname', 'user.organisation')) for item in theses]})
