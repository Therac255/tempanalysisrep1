from a12n.services.sms.sms_action_class import SmsAction


class SmsActionPostSms(SmsAction):
    def __init__(self):
        super().__init__()
        self.action = self.ACTION_SENDSMS
        self.params = {
            'message': None,
            'target': None,
            'phl_codename': None,
            'sender': None,
            'post_id': None,
            'period': None,
            'time_period': None,
            'time_local': None,
            'autotrimtext': None,
            'sms_type': None,
            'wap_url': None,
            'wap_expires': None,
        }

    def validate_params(self, params=None):

        phl_codename, target = params.get('phl_codename'), params.get('target')
        sms_type, wap_url = params.get('sms_type'), params.get('wap_url')

        if phl_codename and target:
            raise Exception('Несовместимые параметры в одном запросе: phl_codename, target')
        if wap_url and sms_type != 'W':
            raise Exception('wap_url using for sms_type = W only')
        return True
