from flask import Flask

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import api
    app.register_blueprint(api.api_bp)

    
    print("setting embed model")
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core import Settings

    embed_model_name = app.config["EMBED_MODEL_NAME"]
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embed_model_name
    )

    return app