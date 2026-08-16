from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, PositiveInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class NewItemData(BaseModel):
    """ """

    name: str | None = None
    description: str | None = None
    price: Annotated[Decimal | None, Field(max_digits=16, decimal_places=8, ge=0)] = None


class UpdateItemRequest(BaseModel):
    """ """

    id: PositiveInt
    new_data: NewItemData


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
        item: ItemDTO = await self.item_repo.update(request_object.id, request_object.new_data)
        return UpdateItemResponse.model_construct(**item.model_dump())
