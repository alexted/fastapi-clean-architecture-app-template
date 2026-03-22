from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Response, APIRouter, status

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
from src.domain.use_cases.items.list_items import ListItemsUseCase, ListItemsResponse

if TYPE_CHECKING:
    from pydantic import PositiveInt

    from src.domain.use_cases.items.update_item import NewItemData

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


@routes.get("/items")
async def list_items(use_case: Annotated[ListItemsUseCase, Depends(ListItemsUseCase)]) -> list[ListItemsResponse]:
    """
    List items
    :param use_case:
    :return:
    """
    items: list[ListItemsResponse] = await use_case.execute()
    return items


@routes.put("/items/{item_id}")
async def update_item(
    item_id: PositiveInt, new_item_data: NewItemData, use_case: Annotated[UpdateItemUseCase, Depends(UpdateItemUseCase)]
) -> UpdateItemResponse:
    """
    Update item
    :param item_id:
    :param new_item_data:
    :param use_case:
    :return:
    """
    req = UpdateItemRequest(item_id, new_item_data)
    item: UpdateItemResponse = await use_case.execute(req)
    return item


@routes.delete("/items/{item_id}")
async def delete_item(
        item_id: PositiveInt, use_case: Annotated[DeleteItemUseCase, Depends(DeleteItemUseCase)]
) -> Response:
    """
    Delete item
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: DeleteItemRequest = DeleteItemRequest(id=item_id)
    await use_case.execute(request_object)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
