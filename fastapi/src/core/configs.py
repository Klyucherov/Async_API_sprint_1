import os

from pydantic import BaseSettings
from pydantic.fields import Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(BaseSettings):

    class Config:
        env_file = os.path.join(BASE_DIR, '../../.env')
        env_file_encoding = 'utf-8'


class ConnectionConfig(BaseConfig):

    redis_host: str = Field(env='REDIS_HOST')
    redis_port: int = Field(env='REDIS_PORT')

    elastic_host: str = Field(env='ELASTIC_HOST')
    elastic_port: int = Field(env='ELASTIC_PORT')


class LogConfig(BaseConfig):

    CONSOLE_LOG_LEVEL: str = Field(env='CONSOLE_LOG_LEVEL')
    UVICORN_LOG_LEVEL: str = Field(env='UVICORN_LOG_LEVEL')
    ROOT_LOG_LEVEL: str = Field(env='ROOT_LOG_LEVEL')
