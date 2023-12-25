from a12n.services.sms import SmsActionPostSms, SmsActionStatus, SmsClient


class ServiceSMS:
    def __init__(self, user, password):

        self.sms_client = SmsClient(
            user,
            password,
            'POST',
        )

    def start_multipost(self):
        self.sms_client.start_multipost()

    def process(self):
        return self.sms_client.send_request()

    def post_mes(self, mes, target, sender, phl_codename=None, post_id=None, period=None):
        action = SmsActionPostSms()
        action.set_params({
            'message': mes,
            'target': target,
            'sender': sender,
        })
        self.sms_client.set_action(action)
        if not self.sms_client.is_multipost():
            return self.sms_client.send_request()

    def post_message(self, mes, target, sender=None, post_id=None, period=False):
        return self.post_mes(mes, target, False, sender, post_id, period)

    def post_message_phl(self, mes, phl_codename, sender=None, post_id=None, period=False):
        return self.post_mes(mes, False, phl_codename, sender, post_id, period)

    def status_sms(self, date_from, date_to, smstype, sms_group_id, sms_id):
        action = SmsActionStatus()
        action.set_params({
            'sms_id': sms_id,
            'date_from': date_from,
            'date_to': date_to,
            'smstype': smstype,
            'sms_group_id': sms_group_id,
        })
        self.sms_client.set_action(action)
        if not self.sms_client.is_multipost():
            return self.sms_client.send_request()

    def status_sms_id(self, sms_id):
        return self.status_sms(None, None, None, None, sms_id)

    def status_sms_group_id(self, sms_group_id):
        return self.status_sms(None, None, None, sms_group_id, None)

    def status_sms_date(self, date_from, date_to, smstype='SENDSMS'):
        return self.status_sms(date_from, date_to, smstype, None, None)
#
