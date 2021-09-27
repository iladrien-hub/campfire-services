import requests
from dataclasses import dataclass
from rest_framework import authentication, exceptions

from BlogService.settings import USER_SERVICE_ADDR


@dataclass
class Account:
    id: int
    username: str
    is_authenticated: bool


class UserServiceAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise exceptions.AuthenticationFailed('Credentials was not provided')

        r = requests.post(f'http://{USER_SERVICE_ADDR}:8000/api/v0/jwt-token-verify', headers={
            "Authorization": token
        })
        if r.status_code != 200:
            raise exceptions.AuthenticationFailed(r.json().get("detail", "Authentication failed"))

        user = Account(is_authenticated=True, **r.json())

        return user, None

