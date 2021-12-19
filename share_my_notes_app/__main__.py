from flask import Flask

from share_my_notes_app.data_access_layer.database_connection import DatabaseConnection

from share_my_notes_app.web_api.api.notes import NotesApi


if __name__ == "__main__":
    db_connection = DatabaseConnection()

    NotesApi.configure_db(db_connection.get_engine())
    app = Flask(__name__)
    NotesApi.register_routes(app)

    app.run()
