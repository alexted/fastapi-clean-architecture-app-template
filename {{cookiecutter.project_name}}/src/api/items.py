from fastapi import APIRouter, Depends, Response, status
from pydantic import NonNegativeInt

from src.use_cases.items.create_item import (
    get_create_item_use_case,
    CreateItemRequest,
    CreateItemResponse,
    CreateItemUseCase
)
from src.use_cases.items.delete_item import (
    get_delete_item_use_case,
    DeleteItemRequest,
    DeleteItemUseCase
)
from src.use_cases.items.get_item import (
    get_item_use_case,
    GetItemRequest,
    GetItemResponse,
    GetItemUseCase
)
from src.use_cases.items.update_item import (
    get_update_item_use_case,
    UpdateItemRequest,
    UpdateItemResponse,
    UpdateItemUseCase
)

routes = APIRouter(tags=['items'])


@routes.post('/items', response_model=CreateItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: CreateItemRequest,
                      use_case: CreateItemUseCase = Depends(get_create_item_use_case)) -> CreateItemResponse:
    """
    Create item
    :param item:
    :param use_case:
    :return:
    """
    item: CreateItemResponse = await use_case.execute(item)
    return item


@routes.get('/items/{item_id}', response_model=GetItemResponse)
async def get_item(item_id: NonNegativeInt, use_case: GetItemUseCase = Depends(get_item_use_case)) -> GetItemResponse:
    """
    Get item by id
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: GetItemRequest = GetItemRequest(id=item_id)
    item: GetItemResponse = await use_case.execute(request_object)
    return item


@routes.put('/items/{item_id}', response_model=UpdateItemResponse)
async def update_item(
        item: UpdateItemRequest, use_case: UpdateItemUseCase = Depends(get_update_item_use_case)
) -> UpdateItemResponse:
    """
    Update item
    :param item:
    :param use_case:
    :return:
    """
    item: UpdateItemResponse = await use_case.execute(item)
    return item


@routes.delete('/items/{item_id}')
async def delete_item(item_id: NonNegativeInt, use_case: DeleteItemUseCase = Depends(get_delete_item_use_case)):
    """
    Delete item
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: DeleteItemRequest = DeleteItemRequest(id=item_id)
    await use_case.execute(request_object)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
