import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.environ.get("ENV", "")


class Settings(BaseSettings):
    service_name: str = Field("", alias='SERVICE_NAME')
    common: str = Field("", alias='COMMON')

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        env_file=('.env', f'.env.{env}'),
        extra='ignore'
    )


settings = Settings(_env_file_encoding='utf-8')