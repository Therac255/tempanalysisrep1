from rest_framework.views import exception_handler
from rest_framework import response as drf_response, status
from django.db import IntegrityError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = status.HTTP_400_BAD_REQUEST

    if not response and isinstance(exc, IntegrityError):
        response = drf_response.Response(
            {
                'message': exc.args[0]
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
