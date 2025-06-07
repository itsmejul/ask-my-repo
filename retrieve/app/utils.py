import redis
from datetime import datetime


def within_budget():
    '''
    Check whether a groq api request is over a threshold per month
    '''
    redis_host = current_app.config["REDIS_HOST"]
    redis_port = current_app.config["REDIS_PORT"]
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    key = f"usage:{datetime.now().strftime('%Y-%m')}"
    usage = int (r.get(key) or 0 )
    if usage >= 1000: # Max number of requests per month
        return False
    r.incr(key)
    return True