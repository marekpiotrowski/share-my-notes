import pathlib

from flask import Flask

from share_my_notes_app.data_access_layer.database_connection import DatabaseConnection

from share_my_notes_app.web_app.api.note import NoteApi
from share_my_notes_app.web_app.api.session import SessionApi
from share_my_notes_app.web_app.index import Index


if __name__ == "__main__":
    template_dir = pathlib.Path(__file__).parent.resolve() / 'web_app' / 'templates'
    app = Flask(__name__, template_folder=template_dir)

    db_connection = DatabaseConnection()

    NoteApi.configure_db(db_connection.get_engine())
    SessionApi.configure_db(db_connection.get_engine())

    NoteApi.register_routes(app)
    SessionApi.register_routes(app)
    Index.register_routes(app)

    app.run()
