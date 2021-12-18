import os

from sqlalchemy import create_engine, text

from share_my_notes_app.data_access_layer.model import mapper_registry

# "mysql+pymysql://root:my-secret-pw@172.17.0.2/share_my_notes_db?charset=utf8mb4"

class DataAccessLayer:
    @staticmethod
    def __drop_db():
        for tbl in reversed(mapper_registry.metadata.sorted_tables):
            engine.execute(tbl.delete())

    @staticmethod
    def bootstrap_db():
        connection_string = os.getenv('DB_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("Empty connection string.")

        engine = create_engine(connection_string)

        mapper_registry.metadata.create_all(engine)

        with engine.connect() as conn:
            result = conn.execute(text("show tables;"))
            print(result.all())
