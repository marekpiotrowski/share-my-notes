import unittest
import os

from share_my_notes_app.data_access_layer.database_connection import DatabaseConnection


class TestDatabaseConnection(unittest.TestCase):

    def test_empty_connection_string_supplied(self):
        os.environ['DB_CONNECTION_STRING'] = ''
        with self.assertRaises(ValueError):
            DatabaseConnection()

if __name__ == '__main__':
    unittest.main()
