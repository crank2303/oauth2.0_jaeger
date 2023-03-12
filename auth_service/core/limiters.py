from flask import jsonify, request
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from http import HTTPStatus

from core.settings import settings
from database.cache_redis import redis_app

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.limiter_config],
    storage_uri="memory://",
)


def rate_limit():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            pipline = redis_app.pipeline()
            now = datetime.now()
            key = f"{request.remote_addr}:{now.minute}"
            pipline.incr(key, 1)
            pipline.expire(key, 59)
            request_number = pipline.execute()[0]
            if request_number > settings.limiter_count:
                return jsonify(
                    msg="Too many requests"), HTTPStatus.TOO_MANY_REQUESTS
            return func(*args, **kwargs)
        return inner
    return wrapper
