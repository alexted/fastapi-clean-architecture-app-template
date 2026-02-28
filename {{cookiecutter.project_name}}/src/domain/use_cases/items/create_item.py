from typing import Annotated
from decimal import Decimal

from fastapi import Depends
from pydantic import Field, BaseModel, PositiveInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class CreateItemRequest(BaseModel):
    """ """

    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class CreateItemResponse(BaseModel):
    """ """

    id: PositiveInt
    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class CreateItemUseCase(BaseUseCase):
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]) -> None:
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: CreateItemRequest) -> CreateItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.create(request_object)
        return CreateItemResponse.model_construct(**item.model_dump())
