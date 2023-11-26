import jwt
import time
from functools import wraps
from flask import request

# dummy secret key
SECRET="oiIGTnmD4AdBYgvPnjJXqUF8igiWZccd"

def create_token(payload):
    payload['exp']=time.time() + 300
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token

def decode_token(token):
    payload=jwt.decode(token, SECRET, algorithms=["HS256"])
    return payload

def jwt_required():
    def decorator(func):
        wraps(func)
        def wrapper(*args, **kwargs):
            if (request.method)=="POST":
                return func(*args, **kwargs)
            else:
                bearer_token = request.headers.get('Authorization')
                
                if not bearer_token:
                    return "Token required!", 401
                token = bearer_token.split(" ")
                if len(token)!=2:
                    return "Invalid token!", 401
                try:
                    decode_token(token[1])
                except jwt.exceptions.ExpiredSignatureError:
                    return "Token expired", 401
                except:
                    return "Invalid token!", 401
                return func(*args, **kwargs)
                

        return wrapper
    return decorator
