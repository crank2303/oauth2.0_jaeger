from functools import wraps
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            match role:
                case "admin":
                    if claims["is_administrator"]:
                        return fn(*args, **kwargs)
                    return jsonify(msg="Admins only!"), HTTPStatus.FORBIDDEN 
                case "manager":
                    if claims["is_administrator"] or \
                            claims["is_manager"]:
                        return fn(*args, **kwargs)
                    return jsonify(msg="Admins and managers only!"), HTTPStatus.FORBIDDEN 

        return decorator

    return wrapper