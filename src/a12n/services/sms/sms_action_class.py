from abc import ABC, abstractmethod


class SmsAction(ABC):
    ACTION_SENDSMS = 'post_sms'
    ACTION_STATUS = 'status'

    def __init__(self):
        self.action = None
        self.params = {}
        self.error_params = []

    @abstractmethod
    def validate_params(self, params=None):
        pass

    def set_params(self, params=None):
        if not self.validate_params(params):
            return self.error_params

        if params:
            for key, param in params.items():
                if key in self.params:
                    self.params[key] = param

        return True

    def get_action_name(self):
        return self.action

    def form_post_fields(self):
        post_fields = {'action': self.get_action_name()}
        post_fields.update(self.params)
        return post_fields
