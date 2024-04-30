from {{ cookiecutter.project_slug }}.api.serializers.items import ItemRequest, ItemResponse
from {{ cookiecutter.project_slug }}.data.postgres.repository.item import ItemRepo
from {{ cookiecutter.project_slug }}.data.postgres.repository.item_dto import ItemDTO
from {{ cookiecutter.project_slug }}.use_cases.base import BaseUseCase


class CreateUser(BaseUseCase):
    def __init__(self, item_repo: ItemRepo):
        self.item_repo: ItemRepo = item_repo

    async def execute(self, request_object: ItemRequest) -> ItemResponse:
        item: ItemDTO = await self.item_repo.add(request_object)
        return item


async def get_create_item_use_case() -> CreateUser:
    return CreateUser(ItemRepo())
