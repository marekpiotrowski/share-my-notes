import json

from share_my_notes_app.data_access_layer.model import Note
from sqlalchemy.orm import Session


class NotesApi:
    @staticmethod
    def configure_db(engine):
        NotesApi.__engine = engine

    @staticmethod
    def register_routes(app):
        app.add_url_rule('/notes', view_func=NotesApi.__get_all_notes)

    @staticmethod
    def __get_all_notes() -> dict:
        with Session(NotesApi.__engine) as session:
            notes = session.query(Note).all()
        return json.dumps(notes)
