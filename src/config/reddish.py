import redis
from decouple import config as decouple_config

REDIS_HOST = decouple_config("REDIS_HOST", default="")
REDIS_PORT = decouple_config("REDIS_PORT", default="")

if REDIS_HOST == "":
    raise NotImplementedError("REDIS_HOST needs to be set.")

if REDIS_PORT == "":
    raise NotImplementedError("REDIS_PORT needs to be set.")


redis_client = redis.Redis(
    host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True, db=0
)
