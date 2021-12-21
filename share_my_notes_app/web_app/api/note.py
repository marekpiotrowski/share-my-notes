import json
import datetime

from sqlalchemy.orm import Session as SqlSession
from flask import request

from share_my_notes_app.data_access_layer.model import Note
from share_my_notes_app.web_app.api.alchemy_encoder import AlchemyEncoder

class NoteApi:
    @staticmethod
    def configure_db(engine):
        NoteApi.__engine = engine

    @staticmethod
    def register_routes(app):
        app.add_url_rule('/notes', view_func=NoteApi.__get_all_notes)
        app.add_url_rule('/notes/session/<int:session_id>', view_func=NoteApi.__get_sessions_notes)
        app.add_url_rule('/note', view_func=NoteApi.__add_note, methods=['POST'])

    @staticmethod
    def __get_all_notes() -> dict:
        with SqlSession(NoteApi.__engine) as session:
            notes = session.query(Note).all()
        return json.dumps(notes, cls=AlchemyEncoder)

    @staticmethod
    def __get_sessions_notes(session_id) -> dict:
        with SqlSession(NoteApi.__engine) as session:
            notes = session.query(Note).filter(Note.session_id == session_id).all()
        return json.dumps(notes, cls=AlchemyEncoder)

    @staticmethod
    def __add_note() -> dict:
        if request.method == 'POST':
            note_data = request.get_json(silent=True)
            new_note = Note(content=note_data['content'],
                            session_id=note_data['sessionId'],
                            title=note_data['title'],
                            expires_on=datetime.datetime.utcnow() + datetime.timedelta(days=7),
                            created_date=datetime.datetime.utcnow())
            with SqlSession(NoteApi.__engine) as sql_session:
                sql_session.add(new_note)
                sql_session.commit()
                sql_session.refresh(new_note)
                print(json.dumps(new_note, cls=AlchemyEncoder))
            return json.dumps(new_note, cls=AlchemyEncoder)
