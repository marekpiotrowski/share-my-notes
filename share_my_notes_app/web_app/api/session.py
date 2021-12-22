import json
from passlib.hash import sha256_crypt

from sqlalchemy.orm import Session as SqlSession
from sqlalchemy.orm import load_only
from flask import request, Response

from share_my_notes_app.data_access_layer.model import Session
from share_my_notes_app.web_app.api.alchemy_encoder import AlchemyEncoder


class SessionApi:
    @staticmethod
    def configure_db(engine):
        SessionApi.__engine = engine

    @staticmethod
    def register_routes(app):
        app.add_url_rule('/sessions', view_func=SessionApi.__get_all_sessions)
        app.add_url_rule('/session', view_func=SessionApi.__add_get_session, methods=['POST', 'GET'])


    @staticmethod
    def __get_all_sessions() -> dict:
        with SqlSession(SessionApi.__engine) as session:
            sessions = session.query(Session).options(load_only("name", "id")).all()
            return json.dumps(sessions, cls=AlchemyEncoder)

    @staticmethod
    def __add_get_session() -> dict:
        if request.method == 'POST':
            content = request.get_json(silent=True)
            pwd_hash = sha256_crypt.encrypt(content['password'])
            new_session = Session(name=content['name'], password=pwd_hash)
            with SqlSession(SessionApi.__engine) as sql_session:
                sql_session.add(new_session)
                sql_session.commit()
                sql_session.refresh(new_session)
                # TODO would make sense to remove 'password'
                return json.dumps(new_session, cls=AlchemyEncoder)
        elif request.method == "GET":
            session_name = request.args.get('name')
            supplied_password = request.args.get('password')
            with SqlSession(SessionApi.__engine) as session:
                result = session.query(Session).options(load_only("name", "id")).filter(Session.name == session_name).first()
                if not sha256_crypt.verify(supplied_password, result.password):
                    return Response('Access denied', 401)
                return json.dumps(result, cls=AlchemyEncoder)
