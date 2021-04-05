from flask import Flask


def create_app():
    app = Flask(__name__)
    with app.app_context():
        from api import routes
        app.register_blueprint(routes.scrapper_bp)
    return app


