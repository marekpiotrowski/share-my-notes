import os

from sqlalchemy import create_engine, text

from share_my_notes_app.data_access_layer.model import mapper_registry

# "mysql+pymysql://root:my-secret-pw@172.17.0.2/share_my_notes_db?charset=utf8mb4"

class DatabaseConnection:
    def __init__(self):
        connection_string = os.getenv('DB_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("Empty connection string.")

        self.__engine = create_engine(connection_string, echo=True)

        mapper_registry.metadata.create_all(self.__engine)

    # def __drop_db(self):
        # for tbl in reversed(mapper_registry.metadata.sorted_tables):
            # engine.execute(tbl.delete())

    def get_engine(self):
        return self.__engine

        # with engine.connect() as conn:
            # result = conn.execute(text("show tables;"))
            # print(result.all())
