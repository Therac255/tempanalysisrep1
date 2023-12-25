from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.response import Response


def paginate_queryset(self, queryset):
    """
    Paginates a given queryset.
    """
    page = self.paginator.paginate_queryset(queryset, self.request, view=self)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)


def generate_otp_code():
    """
    Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
    Default token length = 6
    """
    token_length = getattr(settings, "OTP_LENGTH", 6)
    return get_random_string(token_length, allowed_chars="0123456789")


def generate_password():
    """
    Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
    Default token length = 6
    """
    token_length = getattr(settings, "PASSWORD_LENGTH", 8)
    return get_random_string(
        token_length,
        allowed_chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&+=*"
    )
