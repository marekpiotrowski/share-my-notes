import json

from sqlalchemy.orm import Session as SqlSession
from flask import request

from share_my_notes_app.data_access_layer.model import Session
from share_my_notes_app.web_app.api.alchemy_encoder import AlchemyEncoder


class SessionApi:
    @staticmethod
    def configure_db(engine):
        SessionApi.__engine = engine

    @staticmethod
    def register_routes(app):
        app.add_url_rule('/sessions', view_func=SessionApi.__get_all_sessions)
        app.add_url_rule('/session', view_func=SessionApi.__add_session, methods=['POST'])


    @staticmethod
    def __get_all_sessions() -> dict:
        with SqlSession(SessionApi.__engine) as session:
            sessions = session.query(Session).all()
        return json.dumps(sessions, cls=AlchemyEncoder)

    @staticmethod
    def __add_session() -> dict:
        if request.method == 'POST':
            content = request.get_json(silent=True)
            new_session = Session(name=content['name'], password=content['password'])
            with SqlSession(SessionApi.__engine) as sql_session:
                sql_session.add(new_session)
                sql_session.commit()
                sql_session.refresh(new_session)
            return json.dumps(new_session, cls=AlchemyEncoder)
