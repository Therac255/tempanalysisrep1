from abc import ABC, abstractmethod


class SmsActionInterface(ABC):
    @abstractmethod
    def get_action_name(self) -> str:
        pass

    @abstractmethod
    def set_params(self, params: dict):
        pass

    @abstractmethod
    def form_post_fields(self) -> dict:
        pass

    @abstractmethod
    def validate_params(self, params: dict):
        pass
