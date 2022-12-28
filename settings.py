import os
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str = ''
    base_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_url: str = '/static/'
    static_root: str = os.path.join(base_root, 'static')
    database_pool_size: int = 1
    time_zone: str = 'Europe/Moscow'
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

