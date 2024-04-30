import contextlib
import functools

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Query

from {{ cookiecutter.project_slug }}.app.config import config

engine = create_async_engine(
    config.POSTGRES_DSN,
    pool_size=config.POSTGRES_MAX_CONNECTIONS,
    pool_pre_ping=True,
    pool_recycle=60,
)
OurSession = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@contextlib.asynccontextmanager
async def session_scope(session_class=OurSession, query_class=Query):
    session: AsyncSession = session_class(query_cls=query_class)

    try:
        yield session

        await session.commit()
    except Exception as ex:
        await session.rollback()

        raise ex
    finally:
        await session.close()


def db_session(f):
    """
    Alternative to session_scope.
    Use as a decorator - automatically passes the session to the function's arguments, and make commit when it is over.

    >>> @db_session
    >>> def update_entity(entity_id, session: AsyncSession):
    >>>     entity = session.query(Entity).filter_by(id=entity_id)
    >>>     entity.value = 'new-value'
    >>>     session.add(entitity)
    """

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        if 'session' not in kwargs and all(not isinstance(arg, AsyncSession) for arg in args):
            async with session_scope() as session:
                return await f(*args, session=session, **kwargs)
        else:
            return await f(*args, **kwargs)

    return wrapper
