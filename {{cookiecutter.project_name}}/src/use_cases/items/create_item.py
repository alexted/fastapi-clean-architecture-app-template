from pydantic import NonNegativeInt

from src.data.postgres.repository.item import ItemRepository
from src.data.postgres.repository.item_dto import ItemDTO
from pydantic import BaseModel
from src.use_cases.base import BaseUseCase


class CreateItemRequest(BaseModel):
    """

    """
    name: str
    description: str
    price: NonNegativeInt


class CreateItemResponse(BaseModel):
    """

    """
    id: NonNegativeInt
    name: str
    description: str
    price: NonNegativeInt


class CreateItemUseCase(BaseUseCase):
    """

    """
    def __init__(self, item_repo: ItemRepository):
        self.item_repo: ItemRepository = item_repo

    async def execute(self, request_object: CreateItemRequest) -> CreateItemResponse:
        """

        :param request_object:
        :return:
        """
        item: ItemDTO = await self.item_repo.create(request_object)
        return CreateItemResponse.construct(**item.dict())


async def get_create_item_use_case() -> CreateItemUseCase:
    """

    :return:
    """
    return CreateItemUseCase(ItemRepository())
