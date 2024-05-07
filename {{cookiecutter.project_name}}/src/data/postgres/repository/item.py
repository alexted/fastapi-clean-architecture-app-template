import logging
import typing as t

from sqlalchemy import insert, literal_column, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.data.postgres.engine import db_session
from src.data.postgres.models import Item
from src.data.postgres.repository.base_repo import AbstractRepository
from src.data.postgres.repository.item_dto import ItemDTO
from src.data.postgres.repository.item_dto import ItemFilters

logger = logging.getLogger()


class ItemRepository(AbstractRepository):
    """

    """
    def convert_to_dto(self, obj) -> ItemDTO:
        """

        :param obj:
        :return:
        """
        return ItemDTO.from_orm(obj)

    @db_session
    async def create(self, obj_data, session: AsyncSession) -> ItemDTO:
        """

        :param obj_data:
        :param session:
        :return:
        """
        item_data = obj_data.dict()

        stmt = insert(Item).values(**item_data).returning(Item)

        result = (await session.execute(stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)

    @db_session
    async def get(self, filters: ItemFilters = None, session: AsyncSession = None) -> t.List[ItemDTO]:
        """

        :param filters:
        :param session:
        :return:
        """

        query = select(Item).options(selectinload("*"))

        if filters:
            if filters.ids:
                query = query.where(Item.id.in_(filters.ids))

        result = (await session.execute(query)).scalars().all()

        return [self.convert_to_dto(res) for res in result]

    @db_session
    async def update(self, item_id: int, data, session: AsyncSession) -> ItemDTO:
        """

        :param item_id:
        :param data:
        :param session:
        :return:
        """
        orm_stmt = update(Item).where(Item.id == item_id).values(data.dict()).returning(Item)

        result = (await session.execute(orm_stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)

    @db_session
    async def delete(self, item_id: int, session: AsyncSession) -> ItemDTO:
        """

        :param item_id:
        :param session:
        :return:
        """

        orm_stmt = delete(Item).where(Item.id == item_id).execution_options(populate_existing=True)

        result = (await session.execute(orm_stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)
