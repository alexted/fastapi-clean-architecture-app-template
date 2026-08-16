from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, PositiveInt

from src.data.items import ItemRepository
from src.domain.use_cases.base import BaseUseCase


class DeleteItemRequest(BaseModel):
    """ """

    id: PositiveInt


class DeleteItemUseCase(BaseUseCase):
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]) -> None:
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: DeleteItemRequest) -> None:
        """

        :param request_object:
        :return:
        """
        await self.item_repo.delete(request_object.id)
