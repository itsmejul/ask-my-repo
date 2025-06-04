## Flask backend
We use a flask backend which can be started (in the flask-service directory) via
``$flask --app backend run --host=0.0.0.0``



## Microservices
Gateway: Processes requests from frontend, especially checks (in the pg database) whether the requested repository has already been indexed, then calls either retrieval or indexing ms depending on that
Retrieval: Performs retrieval on the qdrant database using a query
Indexing: Responsible for starting celery jobs that index repos

TODO: periodically check (from FE) whether the indexing is complete so we can start querying
- method that checks whether a repo is already indexed