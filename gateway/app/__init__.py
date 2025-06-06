from flask import Flask

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from flask_cors import CORS
     # Allow CORS from your frontend container
    CORS(app, origins=["http://localhost:8010"])  # TODO add the real domain where it will run here later

    from app.routes import api
    app.register_blueprint(api.api_bp)

    return app
