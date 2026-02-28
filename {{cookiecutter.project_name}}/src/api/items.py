from typing import Annotated

from fastapi import Depends, Response, APIRouter, status
from pydantic import PositiveInt

from src.domain.use_cases.items import (
    GetItemRequest,
    GetItemUseCase,
    GetItemResponse,
    CreateItemRequest,
    CreateItemUseCase,
    DeleteItemRequest,
    DeleteItemUseCase,
    UpdateItemRequest,
    UpdateItemUseCase,
    CreateItemResponse,
    UpdateItemResponse,
)

routes = APIRouter(tags=["items"])


@routes.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: CreateItemRequest, use_case: Annotated[CreateItemUseCase, Depends(CreateItemUseCase)]
) -> CreateItemResponse:
    """
    Create item
    :param item:
    :param use_case:
    :return:
    """
    item: CreateItemResponse = await use_case.execute(item)
    return item


@routes.get("/items/{item_id}")
async def get_item(
    item_id: PositiveInt, use_case: Annotated[GetItemUseCase, Depends(GetItemUseCase)]
) -> GetItemResponse:
    """
    Get item by id
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: GetItemRequest = GetItemRequest(id=item_id)
    item: GetItemResponse = await use_case.execute(request_object)
    return item


@routes.put("/items/{item_id}")
async def update_item(
    item_id: PositiveInt, item: UpdateItemRequest, use_case: Annotated[UpdateItemUseCase, Depends(UpdateItemUseCase)]
) -> UpdateItemResponse:
    """
    Update item
    :param item_id:
    :param item:
    :param use_case:
    :return:
    """
    item: UpdateItemResponse = await use_case.execute(item)
    return item


@routes.delete("/items/{item_id}")
async def delete_item(item_id: PositiveInt, use_case: Annotated[DeleteItemUseCase, Depends(DeleteItemUseCase)]):
    """
    Delete item
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: DeleteItemRequest = DeleteItemRequest(id=item_id)
    await use_case.execute(request_object)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
