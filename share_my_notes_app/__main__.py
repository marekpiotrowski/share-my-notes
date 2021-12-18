from share_my_notes_app.data_access_layer.data_access_layer import DataAccessLayer
from share_my_notes_app.web_api.app import app


if __name__ == "__main__":
    DataAccessLayer.bootstrap_db()
    print("db ready")
    app.run()
