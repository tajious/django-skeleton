from rest_framework.views import exception_handler
from rest_framework import status


def core_exception_handler(exc, context):

    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
        'PermissionDenied': _handle_authentication_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response


def _handle_authentication_error(exc, context, response):
    response.data = {
        'errors': response.data
    }
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return response
