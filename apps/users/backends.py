from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(token)

    @staticmethod
    def _authenticate_credentials(token):

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.DecodeError:
            message = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(message)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            message = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(message)

        if not user.is_active:
            message = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(message)

        return [user, token]
