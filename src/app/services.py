from abc import abstractmethod, ABCMeta
from typing import Any, Callable, Dict


class BaseService(metaclass=ABCMeta):
    """
    This is a template of a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments

    This is ok:
      @dataclass
      class UserCreator(BaseService):
        first_name: str
        last_name: Optional[str]

        def act(self) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

        # user = UserCreator(first_name='Ivan', last_name='Petrov')()

    This is not ok:
      class UserCreator:
        def __call__(self, first_name: str, last_name: Optional[str]) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    For more implementation examples, check out https://github.com/tough-dev-school/education-backend/tree/master/src/orders/services
    """

    def __call__(self) -> Any:
        self.validate()
        return self.act()

    def get_validators(self) -> list[Callable]:  # noqa
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> Any:
        return NotImplementedError("Please implement in the service class")


class ExternalService:
    def __init__(
        self, framework: Any
    ) -> None:
        self.__framework = framework
    def make_request(
        self,
        url: str,
        data: Dict,
        headers: Dict,
        method: str | None = "post"
    ) -> Any:
        callable_func = getattr(self.__framework, method)
        try:
            resp = callable_func(url, json=data, headers=headers, verify=False)
        except Exception as e:
            raise Exception(e)
        else:
            if not resp.ok:
                raise Exception
            return resp.json()
