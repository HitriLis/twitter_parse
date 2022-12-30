import os
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str
    base_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_pool_size: int = 1
    redis_url: str

    limited_get_tweets: int = 100000
    tweets_key_key_expire: int = 86400
    redis_tweets_key: str = 'get_tweets_key'

    vendor_twitter_api_key: str
    vendor_twitter_api_secret_key: str
    vendor_twitter_api_bearer_token: str
    vendor_twitter_api_access_token: str
    vendor_twitter_api_access_token_secret: str

    def validate(cls, val):
        return str(val).split(',')
    # pylint: enable=E0213

    class Config:
        env_file = '.env'


settings = Settings()

