import unittest
import os
import json

from flask import Flask

from share_my_notes_app.web_app.api.session import SessionApi
from share_my_notes_app.data_access_layer.database_connection import DatabaseConnection


class TestSessionApi(unittest.TestCase):

    def setUp(self):
        os.environ['DB_CONNECTION_STRING'] = 'sqlite://'
        self.db_connection = DatabaseConnection()

    def test_get_sessions_empty_db(self):
        app = Flask(__name__)

        SessionApi.configure_db(self.db_connection.get_engine())
        SessionApi.register_routes(app)

        with app.test_client() as c:
            rv = c.get('/sessions')
            data = json.loads(rv.data)
            assert len(data) == 0

    def test_create_session(self):
        app = Flask(__name__)

        SessionApi.configure_db(self.db_connection.get_engine())
        SessionApi.register_routes(app)

        with app.test_client() as c:
            rv = c.post('/session', json={'name': 'mysessionname', 'password': 'mysessionpassword'})
            rv = c.get('/sessions')
            data = json.loads(rv.data)
            assert len(data) == 1
            assert data[0]['name'] == 'mysessionname'

    def test_session_auth(self):
        app = Flask(__name__)

        SessionApi.configure_db(self.db_connection.get_engine())
        SessionApi.register_routes(app)

        with app.test_client() as c:
            rv = c.post('/session', json={'name': 'mysessionname', 'password': 'mysessionpassword'})
            rv = c.get('/session?name=mysessionname&password=wrongpwd')
            print(rv.status)
            assert rv.status == "401 UNAUTHORIZED"
            rv = c.get('/session?name=mysessionname&password=mysessionpassword')
            assert rv.status == "200 OK"


if __name__ == '__main__':
    unittest.main()
