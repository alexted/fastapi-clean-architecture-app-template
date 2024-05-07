from pydantic import NonNegativeInt

from src.data.postgres.repository.item import ItemRepository
from src.data.postgres.repository.item_dto import ItemDTO
from pydantic import BaseModel
from src.use_cases.base import BaseUseCase


class GetItemRequest(BaseModel):
    """

    """
    id: NonNegativeInt


class GetItemResponse(BaseModel):
    """

    """
    id: NonNegativeInt
    name: str
    description: str
    price: NonNegativeInt


class GetItemUseCase(BaseUseCase):
    """

    """
    def __init__(self, item_repo: ItemRepository):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: GetItemRequest) -> GetItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.get(request_object)
        return GetItemResponse.construct(**item.dict())


async def get_item_use_case() -> GetItemUseCase:
    """

    :return:
    """
    return GetItemUseCase(ItemRepository())
