from functools import wraps
from flask_jwt_extended import get_jwt,jwt_required
from flask import jsonify


# List of Logged out / Invalid Tokens
invalid_tokens = []

# Check the validity of token after logout
def is_jwt_valid():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            global invalid_tokens
            # print("In wrapper:::", invalid_tokens)
            jti = get_jwt()["jti"]
            if jti in invalid_tokens:
                return jsonify(Error="Invalid Token!"), 401
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper