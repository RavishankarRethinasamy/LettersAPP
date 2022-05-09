import jwt

from flask import request
from functools import wraps
from common.config import args


def authorize(f):
    @wraps(f)
    def handler(obj, **kwargs):
        token = request.headers.get("lAuthToken")
        if not token:
            return {'message': 'Token is missing'}
        try:
            kwargs.update(jwt.decode(token, args.get("MAIN.secret_key")))
        except Exception as e:
            return {'message': 'User not authorized.'}, 403

        return f(obj, **kwargs)

    return handler
