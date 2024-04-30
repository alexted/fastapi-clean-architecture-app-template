import abc
import typing as t

from pydantic import BaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def convert_to_dto(self, obj) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, obj_data: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, filters: BaseModel) -> t.List[BaseModel]:
        raise NotImplementedError
