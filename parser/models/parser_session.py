from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from typing import Optional
from .users import User, StatusName
from utils import get_name_from_link

from database.db import Base


class ParserSessionManager:
    def __init__(self, model_cls):
        self.table: sa.Table = model_cls.__table__

    async def create(self, db_session: AsyncSession, links: list, **kwargs):
        """
        Создание сессию парсера базе данных
        """
        obj_db = ParserSession(**kwargs)
        db_session.add(obj_db)
        await db_session.flush()
        db_session.add_all([
            User(
                date_created=datetime.utcnow(),
                username=get_name_from_link(link),
                status=StatusName.pending,
                session_id=obj_db.id
            ) for link in links if get_name_from_link(link)
        ])
        await db_session.flush()
        await db_session.commit()
        return obj_db

    async def get_parser_session(self, session_id: int, db_session: AsyncSession) -> Optional['ParserSession']:
        space_query = sa.select(ParserSession).where(ParserSession.id == session_id).options(
            selectinload(ParserSession.users),
        )

        result = await db_session.execute(space_query)
        parser_session = result.scalars().first()
        return parser_session


class ParserSession(Base):
    __tablename__ = "parser_session"

    id = sa.Column(sa.Integer, primary_key=True)
    date_created = sa.Column(sa.DateTime, server_default=sa.func.now())
    users = relationship('models.users.User', back_populates='session')
    objects: ParserSessionManager = None


ParserSession.objects = ParserSessionManager(model_cls=ParserSession)
