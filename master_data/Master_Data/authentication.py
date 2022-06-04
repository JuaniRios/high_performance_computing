from rest_framework import authentication
import requests

auth_api = "http://127.0.0.1:8000/"


# Custom Authentication using the authentication microservice on port 8000
class ApiAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        # get token string without the Bearer string at the beginning
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            return None

        token = token[7:]
        response = requests.post(auth_api + "token", data={"token": token})
        if response.ok:
            return response.json(), token
        else:
            return None
