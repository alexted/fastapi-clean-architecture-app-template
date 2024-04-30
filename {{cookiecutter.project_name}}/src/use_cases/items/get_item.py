from typing import List

from pydantic import BaseModel

from src.api.serializers.items import ItemResponse
from src.data.postgres.repository.item import ItemRepo
from src.data.postgres.repository.item_dto import ItemFilters, ItemDTO
from src.use_cases.base import BaseUseCase


class GetUserRequest(BaseModel):
    item_id: int


class GetUser(BaseUseCase):
    def __init__(self, items_repo: ItemRepo):
        self.items_repo: ItemRepo = items_repo

    async def execute(self, request_object: GetUserRequest) -> ItemResponse:
        items: List[ItemDTO] = await self.items_repo.get(ItemFilters(ids=[request_object.item_id]))
        return ItemResponse(**items[0].dict())


async def get_get_item_use_case():
    return GetUser(ItemRepo())
