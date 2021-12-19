import json

from sqlalchemy.orm import Session

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

    @staticmethod
    def __get_all_notes() -> dict:
        with Session(NoteApi.__engine) as session:
            notes = session.query(Note).all()
        return json.dumps(notes, cls=AlchemyEncoder)

    @staticmethod
    def __get_sessions_notes(session_id) -> dict:
        with Session(NoteApi.__engine) as session:
            notes = session.query(Note).filter(Note.session_id == session_id).all()
        return json.dumps(notes, cls=AlchemyEncoder)
