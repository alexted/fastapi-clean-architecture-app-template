import logging
import typing as t

from sqlalchemy import insert, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from {{ cookiecutter.project_slug }}.data.postgres.engine import db_session
from {{ cookiecutter.project_slug }}.data.postgres.models import Item
from {{ cookiecutter.project_slug }}.data.postgres.repository.item_dto import ItemDTO
from {{ cookiecutter.project_slug }}.data.postgres.repository.item_dto import ItemFilters
from {{ cookiecutter.project_slug }}.data.postgres.repository.base_repo import AbstractRepository

logger = logging.getLogger(__name__)


class ItemRepo(AbstractRepository):
    def convert_to_dto(self, obj) -> ItemDTO:
        return ItemDTO.from_orm(obj)

    @db_session
    async def add(self, obj_data, session: AsyncSession) -> ItemDTO:
        item_data = obj_data.dict()

        insert_stmt = insert(Item).values(**item_data).returning(literal_column('*'))
        orm_stmt = select(Item).from_statement(insert_stmt).execution_options(populate_existing=True)

        result = (await session.execute(orm_stmt)).scalar_one_or_none()

        return self.convert_to_dto(result)

    @db_session
    async def get(self, filters: ItemFilters = None, session: AsyncSession = None) -> t.List[ItemDTO]:

        query = select(Item).options(selectinload('*'))

        if filters:
            if filters.ids:
                query = query.where(Item.id.in_(filters.ids))

        result = (await session.execute(query)).scalars().all()

        return [self.convert_to_dto(res) for res in result]
