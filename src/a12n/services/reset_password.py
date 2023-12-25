from typing import Any

from a12n.services.base import BaseOTPService
from a12n.tasks import send_message_to_email
from common.common import generate_password


class ResetPassword(BaseOTPService):
    def act(self) -> Any:
        self.reset_password()

    def reset_password(self):
        user = self.get_user('email')
        password = generate_password()
        send_message_to_email(
            subject="Ваш новый пароль",
            email=user.email,
            message=password,
            allow_log=False,
        )
        user.set_password(password)
        user.save()
        return user
