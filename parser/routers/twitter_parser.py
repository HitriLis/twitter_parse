from . import router
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from database.db import get_session
from parser.schemes import ParserCreate, ParserResponse, UserDataResponse
from parser.models import ParserSession
from providers.twitter_conector import twitter_api
from services.parse import parse_users


@router.post("/parse", tags=['Parser session'],
             responses={200: {"model": ParserResponse}})
async def create_parse(item: ParserCreate,  background_tasks: BackgroundTasks, db_session: AsyncSession = Depends(get_session)):
    session = await ParserSession.objects.create(db_session, links=item.links)
    background_tasks.add_task(parse_users, session_id=session.id, db_session=db_session)
    return JSONResponse(status_code=200, content={"session_id": session.id})


@router.get("/users/status/{session_id}", tags=['Parser session'],
            responses={200: {"model": ParserResponse}})
async def get_session(session_id: int, db_session: AsyncSession = Depends(get_session)):
    session = await ParserSession.objects.get_parser_session(session_id, db_session)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Сессия не найдена')

    return JSONResponse(status_code=200, content=ParserResponse.from_orm(session).dict())


@router.get("/users/{username}", tags=['Parser session'],
            responses={200: {"model": UserDataResponse}})
async def get_username(username: str):
    data_user = await twitter_api.get_user_screen_name(username)
    if not data_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Страница не найдена')

    return JSONResponse(status_code=200, content=UserDataResponse(**data_user).dict())


@router.get("/users/tweets/{twitter_id}", tags=['Parser session'],
            responses={200: {"model": UserDataResponse}})
async def get_username(twitter_id: str):
    data_user = await twitter_api.get_tweets(twitter_id)
    if not data_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Страница не найдена')

    return JSONResponse(status_code=200, content=data_user)
