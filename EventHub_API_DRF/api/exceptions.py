from rest_framework import status
from rest_framework.exceptions import APIException


class BusinessAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EventFullError(BusinessAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "No available places."
    default_code = "EVENT_FULL"


class AlreadyRegisteredError(BusinessAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "User is already registered for this event."
    default_code = "ALREADY_REGISTERED"


class NotRegisteredError(BusinessAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "User is not registered for this event."
    default_code = "NOT_REGISTERED"