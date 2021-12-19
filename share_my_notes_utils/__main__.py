import sys

from sqlalchemy.orm import Session as SqlSession

from share_my_notes_app.data_access_layer.model import Note, Session
from share_my_notes_app.data_access_layer.database_connection import DatabaseConnection

def populate_db():
    db_connection = DatabaseConnection()

    with SqlSession(db_connection.get_engine()) as session:
        session_1 = Session(id=1, name="session1", password="pwd1")
        session_2 = Session(id=2, name="session2", password="pwd2")
        session.add(session_1)
        session.add(session_2)
        session.commit()

    with SqlSession(db_connection.get_engine()) as session:
        note_1 = Note(id=1, content="some content 1", session_id=1)
        note_2 = Note(id=2, content="some content 2", session_id=1)
        note_3 = Note(id=3, content="some content 3", session_id=2)
        session.add(note_1)
        session.add(note_2)
        session.add(note_3)
        session.commit()

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "populate_db":
        populate_db()
    else:
        print(f"Unknown command: {cmd}")
        exit(-1)
