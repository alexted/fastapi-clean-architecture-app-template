from typing import Annotated
from pydantic import NonNegativeInt

from src.data.postgres.repository.item import ItemRepository
from pydantic import BaseModel
from src.use_cases.base import BaseUseCase


class DeleteItemRequest(BaseModel):
    """

    """
    id: NonNegativeInt


class DeleteItemUseCase(BaseUseCase):
    """

    """
    def __init__(self, item_repo: Annotated[ItemRepository, Depends(ItemRepository)]):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: DeleteItemRequest) -> bool:
        """

        :param request_object:
        :return:
        """
        await self.item_repo.delete(request_object.id)
        return True
