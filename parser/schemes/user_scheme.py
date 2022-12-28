from pydantic import BaseModel


class UserDataResponse(BaseModel):
    twitter_id: int
    name: str
    username: str
    followers_count: int
    description: str
