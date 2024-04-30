from fastapi import APIRouter, Depends

from {{ cookiecutter.project_slug }}.api.serializers.items import ItemRequest, ItemResponse
from {{ cookiecutter.project_slug }}.use_cases.items.create_item import get_create_item_use_case, CreateUser
from {{ cookiecutter.project_slug }}.use_cases.items.get_item import GetUserRequest, get_get_item_use_case, GetUser

routes = APIRouter(tags=['users'])


@routes.post('/items', response_model=ItemResponse)
async def create_item(item: ItemRequest, use_case: CreateUser = Depends(get_create_item_use_case)) -> ItemResponse:
    item: ItemResponse = await use_case.execute(item)
    return item


@routes.get('/items/{item_id}', response_model=ItemResponse)
async def get_item(item_id: int, use_case: GetUser = Depends(get_get_item_use_case)) -> ItemResponse:
    request_object: GetUserRequest = GetUserRequest(item_id=item_id)
    item: ItemResponse = await use_case.execute(request_object)
    return item
