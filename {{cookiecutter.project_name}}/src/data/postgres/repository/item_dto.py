import typing as t

from pydantic import BaseModel, NoneStr

from src.api.serializers.items import ItemResponse


class CreateItemDTO(BaseModel):
    id: int
    name: str
    description: NoneStr
    price: float


class ItemDTO(ItemResponse):
    class Config:
        orm_mode = True


class ItemFilters(BaseModel):
    ids: t.List[int]
