from pydantic import BaseSettings
from pydantic.networks import PostgresDsn


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn = ''

    class Config():
        env_file = '.env'


settings = Settings('.env')
