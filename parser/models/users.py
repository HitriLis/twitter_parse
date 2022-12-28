from datetime import datetime
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database.db import Base


class StatusName(str, Enum):
    success = 'success'
    pending = 'pending'
    failed = 'failed'


class UserManager:
    def __init__(self, model_cls):
        self.table: sa.Table = model_cls.__table__

    async def update(self, db_session: AsyncSession, *args, **kwargs,):
        """
        Обновить твиттер аккаунта базе данных
        """

        return User(**kwargs)


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    date_created = sa.Column(sa.DateTime, server_default=sa.func.now())
    username = sa.Column(sa.String, nullable=True)
    status = sa.Column(sa.String, nullable=True)
    session_id = sa.Column(sa.Integer, sa.ForeignKey('parser_session.id'), nullable=True)
    session = relationship('models.parser_session.ParserSession', back_populates='users')
    objects: UserManager = None


User.objects = UserManager(model_cls=User)
