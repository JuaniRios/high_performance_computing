import base64
import hashlib
import hmac
from .models import User
# my_app/authentication.py
from rest_framework import authentication
from rest_framework import exceptions
import json

# Custom authentication class using the Json Web Token standard (https://jwt.io/)

SECRET_KEY = bytearray('django-insecure-k%y!680%^+l$m$(f&_mn74d+-z(ey650=fe#+z_+u2qe@im#0b',
                       encoding="ascii")


def encode_jwt(user: User):
    HEADER = json.dumps({"alg": "HS256", "typ": "JWT"})
    PAYLOAD = json.dumps({
        "username": user.username,
        "role": user.role.name
    })

    # convert them into b64 strings
    b64_HEADER = base64.b64encode(bytearray(HEADER, encoding="ascii"))
    b64_PAYLOAD = base64.b64encode(bytearray(PAYLOAD, encoding="ascii"))

    # sign them with a secret key
    SIGNATURE = hmac.new(SECRET_KEY, b64_HEADER + b"." + b64_PAYLOAD, hashlib.sha256).hexdigest()

    return f"{b64_HEADER.decode()}.{b64_PAYLOAD.decode()}.{SIGNATURE}"


def verify_jwt(jwt: str, key: bytearray):
    try:
        header, payload, signature = jwt.split(".")
        verification_signature = hmac.new(
            key,
            bytearray(header, encoding="ascii") + b"." + bytearray(payload, encoding="ascii"),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, verification_signature)
    except ValueError:
        return False


def get_jwt_payload(jwt):
    header, payload, signature = jwt.split(".")
    return json.loads(base64.b64decode(payload.encode()))


class JWTAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        # get token string without the Bearer string at the beginning
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None or not verify_jwt(token[7:], SECRET_KEY):
            return None
        else:
            return get_jwt_payload(token), token
