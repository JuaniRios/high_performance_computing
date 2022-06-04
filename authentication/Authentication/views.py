from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, RoleEnum, check_password
from .authentication import encode_jwt, verify_jwt, JWTAuth, SECRET_KEY, get_jwt_payload
from .permissions import IsUser, IsSecretary, IsManager, IsAdministrator

# create in-memory database
users = {"admin": User("admin", "1234", RoleEnum.ADMINISTRATOR)}


# Custom view for changing users
class UserList(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAdministrator]

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if None in [username, password] or role not in ["ADMINISTRATOR", "SECRETARY", "MANAGER"]:
            return Response("Invalid fields. Please submit a username, password, and a valid role",
                            status.HTTP_400_BAD_REQUEST)

        if username in users:
            return Response("Username already exists", status.HTTP_400_BAD_REQUEST)

        try:
            new_user = User(username, password, RoleEnum[role])
        except Exception:
            return Response("Something went terribly wrong", status.HTTP_500_INTERNAL_SERVER_ERROR)

        users[username] = new_user
        return Response(encode_jwt(new_user), status.HTTP_201_CREATED)

    def get(self, request):
        user_list = [str(val) for val in list(users.values())]
        return Response(user_list, status.HTTP_200_OK)

    def delete(self, request):
        username = request.POST.get("username")
        if username in users:
            del users[username]
            return Response("successfully deleted", status.HTTP_200_OK)

        return Response("user not found", status.HTTP_400_BAD_REQUEST)


# Custom view to retrieve get token from data and get data from token
class TokenService(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = []

    # get token from username and password data
    def get(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        # check fields are submitted
        if not (username or password):
            return Response("username and password fields on HTTP Body required", status.HTTP_400_BAD_REQUEST)

        # check user exists
        if username not in users:
            return Response("user not found", status.HTTP_400_BAD_REQUEST)

        user = users[username]

        # check password is correct
        if not check_password(user.password_hash, password):
            return Response("wrong password", status.HTTP_400_BAD_REQUEST)

        token = encode_jwt(user)
        return Response(token, status.HTTP_200_OK)

    # get user data from token
    def post(self, request):
        token = request.POST["token"]
        if not token:
            return Response("token field not found in HTTP body", status.HTTP_400_BAD_REQUEST)

        token_check = verify_jwt(token, key=SECRET_KEY)
        if not token_check:
            return Response("Invalid Token", status.HTTP_400_BAD_REQUEST)

        data = get_jwt_payload(token)
        if data["username"] not in users:
            return Response("Token valid but user is not present", status.HTTP_400_BAD_REQUEST)

        return Response(data, status.HTTP_200_OK)
