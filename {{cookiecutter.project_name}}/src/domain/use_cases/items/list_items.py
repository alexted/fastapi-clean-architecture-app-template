from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, PositiveInt

from src.data.items import ItemDTO, ItemRepository
from src.domain.use_cases.base import BaseUseCase


class ListItemsRequest(BaseModel): ...


class ListItemsResponse(BaseModel):
    """ """

    id: PositiveInt
    name: str
    description: str
    price: Annotated[Decimal, Field(max_digits=16, decimal_places=8, ge=0)]


class ListItemsUseCase(BaseUseCase):
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]) -> None:
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: ListItemsRequest) -> list[ListItemsResponse]:
        """

        :param request_object:
        :return:
        """
        items: list[ItemDTO] = await self.item_repo.get()
        return [ListItemsResponse.model_construct(**item.model_dump()) for item in items]
