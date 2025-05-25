from flask import Flask
from importlib.resources import files
from flask_restful import Api, Resource, request
from flask_cors import CORS

from retrieve import init, clone_and_read

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/repo/*": {"origins": "http://localhost:8000"}}) #Change this to FE adress


class QueryRepo(Resource):
    def post(self):
        try:
            data = request.get_json()
            repo_url = data["repo_url"] 
            query = data["query"]
            res = clone_and_read(repo_url=repo_url, query=query)

            return {"answer": f"{res}"}, 200
        except Exception as e:
            return "internal error: " + str(e)


api.add_resource(QueryRepo, "/repo/query")

init() # Set env variables 

if __name__ == "__main__":
    app.run()#port=5001)
