from typing import Annotated
from decimal import Decimal

from fastapi import Depends
from pydantic import Field, BaseModel, PositiveInt

from src.data.items import ItemDTO, ItemFilters, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class GetItemRequest(BaseModel):
    """ """

    id: PositiveInt


class GetItemResponse(BaseModel):
    """ """

    id: PositiveInt
    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class GetItemUseCase(BaseUseCase):
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]) -> None:
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: GetItemRequest) -> GetItemResponse:
        """

        :param request_object:
        :return:
        """
        item: list[ItemDTO] = await self.item_repo.get(ItemFilters(id=[request_object.id]))
        return GetItemResponse.model_construct(**item[0].model_dump())
