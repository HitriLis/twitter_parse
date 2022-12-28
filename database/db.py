from uuid import uuid4

from asyncpg import Connection as BaseConnection
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings


class Connection(BaseConnection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid4()}__'


database_url = settings.database_url.replace('postgres://', 'postgresql+asyncpg://').replace('postgresql://', 'postgresql+asyncpg://')
engine = create_async_engine(f'{database_url}?prepared_statement_cache_size=0',
                             echo=True, future=True,
                             connect_args={
                                 'statement_cache_size': 0,
                                 'connection_class': Connection,
                             })
Base = declarative_base()


# получение асинхронной сессии к БД
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
