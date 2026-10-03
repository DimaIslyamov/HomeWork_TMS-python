from django.http import Http404

from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler

from .exceptions import BusinessAPIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, BusinessAPIException):
        response.data = {
            "error": {
                "code": exc.get_codes(),
                "message": exc.detail,
                "details": None,
            }
        }

    elif isinstance(exc, ValidationError):
        response.data = {
            "error": {
                "code": "validation_error",
                "message": "Invalid input.",
                "details": response.data,
            }
        }

    elif isinstance(exc, APIException):
        response.data = {
            "error": {
                "code": exc.get_codes(),
                "message": exc.detail,
                "details": None,
            }
        }

    elif isinstance(exc, Http404):
        response.data = {
            "error": {
                "code": "not_found",
                "message": response.data["detail"],
                "details": None,
            }
        }

    return response
