from rest_framework import authentication, exceptions

from rest_framework.authtoken.models import Token


class AppAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get('Authorization')
        if not key:
            raise exceptions.AuthenticationFailed('Token was not provided')
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token')

        return token.user, None
