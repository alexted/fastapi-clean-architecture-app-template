from typing import Annotated

from fastapi import Depends, Response, APIRouter, status
from pydantic import NonNegativeInt

from src.use_cases.items import (
    GetItemRequest,
    GetItemResponse,
    GetItemUseCase,
    CreateItemRequest,
    CreateItemResponse,
    CreateItemUseCase,
    DeleteItemRequest,
    DeleteItemUseCase,
    UpdateItemRequest,
    UpdateItemResponse,
    UpdateItemUseCase
)

routes = APIRouter(tags=["items"])


@routes.post("/items", response_model=CreateItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: CreateItemRequest,
    use_case: Annotated[CreateItemUseCase, Depends(CreateItemUseCase)]
) -> CreateItemResponse:
    """
    Create item
    :param item:
    :param use_case:
    :return:
    """
    item: CreateItemResponse = await use_case.execute(item)
    return item


@routes.get("/items/{item_id}", response_model=GetItemResponse)
async def get_item(
        item_id: NonNegativeInt,
        use_case: Annotated[GetItemUseCase, Depends(GetItemUseCase)]
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


@routes.put("/items/{item_id}", response_model=UpdateItemResponse)
async def update_item(
        item: UpdateItemRequest,
        use_case: Annotated[UpdateItemUseCase, Depends(UpdateItemUseCase)]
) -> UpdateItemResponse:
    """
    Update item
    :param item:
    :param use_case:
    :return:
    """
    item: UpdateItemResponse = await use_case.execute(item)
    return item


@routes.delete("/items/{item_id}")
async def delete_item(item_id: NonNegativeInt, use_case: Annotated[DeleteItemUseCase, Depends(DeleteItemUseCase)]):
    """
    Delete item
    :param item_id:
    :param use_case:
    :return:
    """
    request_object: DeleteItemRequest = DeleteItemRequest(id=item_id)
    await use_case.execute(request_object)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
