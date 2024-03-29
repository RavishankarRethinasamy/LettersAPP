import jwt
import logging
import traceback

from flask import request
from functools import wraps
from common.config import args


def authorize(f):
    @wraps(f)
    def handler(obj, **kwargs):
        token = request.headers.get("lAuthToken")
        try:
            if not token or token == 'null':
                raise Exception("Auth Token missing in the request")
            kwargs.update(jwt.decode(token, args.get("MAIN.secret_key")))
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
        return f(obj, **kwargs)
    return handler