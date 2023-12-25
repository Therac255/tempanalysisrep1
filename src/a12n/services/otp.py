from a12n.services.base import BaseOTPService


class OTPMailSendService(BaseOTPService):

    def act(self):
        self.send_otp('email')
        if self.allow_log:
            self.create_otp('email')


class OTPPhoneSendService(BaseOTPService):

    def act(self):
        self.send_otp('phone')
        if self.allow_log:
            self.create_otp('personal_info__phone_number')


class OTPEmailVerifyService(BaseOTPService):

    def act(self):
        self.verify_otp('email')


class OTPPhoneVerifyService(BaseOTPService):

    def act(self):
        self.verify_otp('personal_info__phone_number')
