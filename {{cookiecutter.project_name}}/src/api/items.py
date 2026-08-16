from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import PositiveInt  # noqa: TC002

from src.domain.use_cases.items import (
    CreateItemRequest,
    CreateItemResponse,
    CreateItemUseCase,
    DeleteItemRequest,
    DeleteItemUseCase,
    GetItemRequest,
    GetItemResponse,
    GetItemUseCase,
    UpdateItemRequest,
    UpdateItemResponse,
    UpdateItemUseCase,
)
from src.domain.use_cases.items.list_items import ListItemsRequest, ListItemsResponse, ListItemsUseCase
from src.domain.use_cases.items.update_item import NewItemData  # noqa: TC001

routes = APIRouter(tags=["items"])


@routes.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: CreateItemRequest, use_case: Annotated[CreateItemUseCase, Depends(CreateItemUseCase)]
) -> CreateItemResponse:
    """
    Create an item
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
    items: list[ListItemsResponse] = await use_case.execute(ListItemsRequest())
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
    req = UpdateItemRequest(id=item_id, new_data=new_item_data)
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
