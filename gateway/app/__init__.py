from flask import Flask

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import api
    app.register_blueprint(api.api_bp)

    return app
