from typing import List
from pydantic import BaseModel


class ParserCreate(BaseModel):
    links: List


class UserParser(BaseModel):
    username: str
    status: str

    class Config:
        orm_mode = True


class ParserResponse(BaseModel):
    id: int
    users: List[UserParser]

    class Config:
        orm_mode = True
