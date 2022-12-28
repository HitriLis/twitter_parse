from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parser.routers.twitter_parser import router as parser_router
from redis import redis


app = FastAPI()

app.include_router(parser_router, prefix="/api")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await redis.connect()


@app.on_event('shutdown')
async def shutdown():
    await redis.disconnect()

