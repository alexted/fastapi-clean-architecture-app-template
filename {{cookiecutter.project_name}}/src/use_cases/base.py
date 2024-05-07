import abc
from typing import Union

from pydantic import BaseModel


class BaseUseCase(abc.ABC):
    @abc.abstractmethod
    def execute(self, request_object: BaseModel) -> Union[BaseModel, None]:
        raise NotImplementedError("Please implement this method")
