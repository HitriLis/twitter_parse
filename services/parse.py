import time
from sqlalchemy.ext.asyncio import AsyncSession
from parser.models import ParserSession, StatusName
from providers.twitter_conector import twitter_api


async def parse_users(session_id: int, db_session: AsyncSession):
    session = await ParserSession.objects.get_parser_session(session_id, db_session)
    for user in session.users:
        data_user = await twitter_api.get_user_screen_name(user.username)
        user.status = StatusName.success if data_user else StatusName.failed
        await db_session.commit()
