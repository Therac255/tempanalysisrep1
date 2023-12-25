from typing import Dict, Optional

from a12n.services.sms.sms_action_class import SmsAction


class SmsActionStatus(SmsAction):
    def __init__(self):
        super().__init__()
        self.action = 'status'
        self.params = {
            'sms_id': None,
            'sms_group_id': None,
            'date_from': None,
            'date_to': None,
        }

    def validate_params(self, params: Optional[Dict[str, str]] = None) -> bool:
        if params is None:
            params = {}

        sms_id = params.get('sms_id')
        sms_group_id = params.get('sms_group_id')
        date_from = params.get('date_from')
        date_to = params.get('date_to')

        if not sms_id and not sms_group_id and (not date_from or not date_to):
            raise Exception('at least one parameter should have value: \n'
                            'sms_id, sms_group_id, date_from, date_to')

        return True
