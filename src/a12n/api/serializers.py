from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.models import update_last_login
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token

from users.enums import UserType


class UsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    user_type = serializers.ChoiceField(choices=UserType.choices)

    @classmethod
    def get_token(cls, user, user_type) -> Token:
        token = super().get_token(user)
        token["user_type"] = user_type
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user, attrs.get("user_type"))

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class VerifyPhoneNumberSerializer(serializers.Serializer):
    """
    Serializer class to verify OTP.
    """
    phone_number = PhoneNumberField(write_only=True)
    otp_code = serializers.CharField(max_length=settings.OTP_LENGTH)


class VerifyEmailSerializer(serializers.Serializer):
    """
    Serializer class to verify OTP.
    """
    email = serializers.EmailField(write_only=True)
    otp_code = serializers.CharField(max_length=settings.OTP_LENGTH)


class SendOtpToPhoneSerializer(serializers.Serializer):
    """
    Serializer class to send OTP to phone number.
    phone number check if not exist
    """
    phone_number = PhoneNumberField(
        required=True,
        write_only=True,
    )


class SendOtpToEmailSerializer(serializers.Serializer):
    """
    Serializer class to send OTP to email.
    email check if not exist
    """
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer class to reset password.
    """
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
