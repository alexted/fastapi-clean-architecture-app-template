from __future__ import annotations

from typing import TYPE_CHECKING, Annotated
import logging

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload

from src.data.base import AbstractRepository

from .dto import ItemDTO, ItemFilters
from ...infrastructure.clients.postgres.engine import get_db_session
from ...infrastructure.clients.postgres.models import Item

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from ...domain.use_cases.items import CreateItemRequest
    from ...domain.use_cases.items.update_item import NewItemData

logger = logging.getLogger()


class ItemRepository(AbstractRepository):
    """Items storage"""

    def __init__(self, db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> None:
        self._session: AsyncSession = db_session

    def convert_to_dto(self, obj: Item) -> ItemDTO:
        """

        :param obj:
        :return:
        """
        return ItemDTO.model_validate(obj)

    async def create(self, obj_data: CreateItemRequest) -> ItemDTO:
        """

        :param obj_data:
        :return:
        """
        item_data = obj_data.model_dump()

        stmt = insert(Item).values(**item_data).returning(Item)

        result = (await self._session.execute(stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)

    async def get(self, filters: ItemFilters = None) -> list[ItemDTO]:
        """

        :param filters:
        :return:
        """

        query = select(Item).options(selectinload("*"))

        if filters and filters.id:
            query = query.where(Item.id.in_(filters.id))

        result = (await self._session.execute(query)).scalars().all()

        return [self.convert_to_dto(res) for res in result]

    async def update(self, item_id: int, data: NewItemData) -> ItemDTO:
        """

        :param item_id:
        :param data:
        :return:
        """
        orm_stmt = update(Item).where(Item.id == item_id).values(data.model_dump()).returning(Item)

        result = (await self._session.execute(orm_stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)

    async def delete(self, item_id: int) -> ItemDTO:
        """

        :param item_id:
        :return:
        """

        orm_stmt = delete(Item).where(Item.id == item_id).execution_options(populate_existing=True)

        result = (await self._session.execute(orm_stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)
