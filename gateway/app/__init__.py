from flask import Flask
from flask_cors import CORS

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Allow CORS from the frontend container
    frontend_host = app.config["FRONTEND_HOST"]
    frontend_port = app.config["FRONTEND_PORT"]
    frontend_url = "http://" + frontend_host + ":" + str(frontend_port)
    CORS(app, origins=[frontend_url])

    from app.routes import api
    app.register_blueprint(api.api_bp)

    return app
