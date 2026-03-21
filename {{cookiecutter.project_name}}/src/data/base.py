from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel

    from src.infrastructure.clients.postgres.models import Base


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def convert_to_dto(self, obj: Base) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, obj_data: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, filters: BaseModel) -> list[BaseModel]:
        raise NotImplementedError
