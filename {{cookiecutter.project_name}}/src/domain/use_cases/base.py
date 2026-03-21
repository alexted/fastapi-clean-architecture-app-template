from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel


class BaseUseCase(abc.ABC):
    @abc.abstractmethod
    def execute(self, request_object: BaseModel) -> BaseModel | None:
        raise NotImplementedError("Please implement this method")
