from typing import Annotated
from decimal import Decimal

from fastapi import Depends
from pydantic import Field, BaseModel, PositiveInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class ItemData(BaseModel):
    """ """

    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class UpdateItemRequest(BaseModel):
    """ """

    id: PositiveInt
    data: ItemData


class UpdateItemResponse(BaseModel):
    """ """

    id: PositiveInt
    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class UpdateItemUseCase(BaseUseCase):
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]) -> None:
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: UpdateItemRequest) -> UpdateItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.update(request_object.id, request_object.data)
        return UpdateItemResponse.model_construct(**item.model_dump())
