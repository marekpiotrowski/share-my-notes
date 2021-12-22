import json
import datetime
from passlib.hash import sha256_crypt

from sqlalchemy.orm import Session as SqlSession
from flask import request, Response
from sqlalchemy import select

from share_my_notes_app.data_access_layer.model import Note, Session
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
        app.add_url_rule('/note/<int:note_id>', view_func=NoteApi.__update_note, methods=['PUT'])

    @staticmethod
    def __get_all_notes() -> dict:
        with SqlSession(NoteApi.__engine) as session:
            notes = session.query(Note).all()
        return json.dumps(notes, cls=AlchemyEncoder)

    @staticmethod
    def __get_sessions_notes(session_id) -> dict:
        # TODO handle expiration...
        supplied_password = request.args.get('password')
        with SqlSession(NoteApi.__engine) as session:
            parent_session = session.query(Session).filter(Session.id == session_id).first()
            if not sha256_crypt.verify(supplied_password, parent_session.password):
                return Response('Access denied', 401)
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
            return json.dumps(new_note, cls=AlchemyEncoder)

    @staticmethod
    def __update_note(note_id) -> dict:
        if request.method == 'PUT':
            note_data = request.get_json(silent=True)
            with SqlSession(NoteApi.__engine) as sql_session:
                edited_note = sql_session.query(Note).filter(Note.id == note_id).first()
                edited_note.content = note_data['content']
                edited_note.title = note_data['title']
                edited_note.expires_on = datetime.datetime.fromisoformat(note_data['expiresOn'])
                sql_session.commit()
                sql_session.refresh(edited_note)
            return json.dumps(edited_note, cls=AlchemyEncoder)
