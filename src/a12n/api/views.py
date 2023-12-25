from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from a12n.api.serializers import (
    ResetPasswordSerializer,
    SendOtpToEmailSerializer,
    SendOtpToPhoneSerializer,
    UsernameTokenObtainPairSerializer,
    VerifyEmailSerializer,
    VerifyPhoneNumberSerializer,
)
from a12n.services.otp import OTPEmailVerifyService, OTPPhoneVerifyService
from a12n.services.reset_password import ResetPassword
from a12n.tasks import send_message_to_email, send_message_to_phone
from common.common import generate_otp_code
from users.enums import UserType


class UsernameTokenObtainPairView(TokenObtainPairView):
    """
    Username Token Obtain Pair View
    This view is used to obtain a JWT token using a username and password.
    """
    serializer_class = UsernameTokenObtainPairSerializer

    @extend_schema(
        request=UsernameTokenObtainPairSerializer,
        parameters=[
            OpenApiParameter(
                'user_type',
                type=str,
                location=OpenApiParameter.QUERY,
                enum=[e.value for e in UserType])  # type: ignore
        ]
    )
    def post(self, request, *args, **kwargs):
        user_type_value = request.query_params.get('user_type')
        request.data["user_type"] = user_type_value
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not self._has_user_type(user, user_type_value):
            return Response(
                data={"detail": f"User is not a {user_type_value} account"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().post(request, *args, **kwargs)

    @staticmethod
    def _has_user_type(user, user_type_value):
        user_type = UserType(user_type_value)
        return hasattr(user, user_type.value.lower())


class OtpView(
    GenericViewSet,
):
    """
    OTP View
    """
    serializer_action_classes = {
        'verify_phone_number': VerifyPhoneNumberSerializer,
        'verify_email': VerifyEmailSerializer,
        'send_otp_to_phone': SendOtpToPhoneSerializer,
        'send_otp_to_email': SendOtpToEmailSerializer,
        'reset_password': ResetPasswordSerializer,
    }
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action)

    @extend_schema(
        request=VerifyPhoneNumberSerializer,
    )
    @action(detail=False, methods=['post'], url_path='phone/verify')
    def verify_phone_number(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']
        OTPPhoneVerifyService(
            contact_value=phone_number,
            message=otp_code
        )()
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=VerifyEmailSerializer,
    )
    @action(detail=False, methods=['post'], url_path='email/verify')
    def verify_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        OTPEmailVerifyService(
            contact_value=email,
            message=otp_code
        )()
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=SendOtpToPhoneSerializer,
    )
    @action(detail=False, methods=['post'], url_path='phone/send')
    def send_otp_to_phone(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        send_message_to_phone(
            phone_number=phone_number,
            message=generate_otp_code()
        )
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=SendOtpToEmailSerializer,
    )
    @action(detail=False, methods=['post'], url_path='email/send')
    def send_otp_to_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        send_message_to_email(
            subject="Код подтверждения",
            email=email,
            message=generate_otp_code(),
        )
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=ResetPasswordSerializer,
    )
    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        ResetPassword(
            contact_value=email
        )()
        return Response(status=status.HTTP_200_OK)
