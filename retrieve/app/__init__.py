from flask import Flask

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import api
    app.register_blueprint(api.api_bp)

    
    print("setting embed model")
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core import Settings
    #TODO move this outside
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return app