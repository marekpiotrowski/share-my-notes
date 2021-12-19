from flask import render_template


class Index:
    @staticmethod
    def register_routes(app):
        app.add_url_rule('/', view_func=Index.__index)

    @staticmethod
    def __index():
        return render_template('index.html')
