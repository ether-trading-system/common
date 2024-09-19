import os

from typing import Dict
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

env = os.environ.get("ENV", "")


class DiscordTopic(BaseModel):
    name: str = Field(default='Unknown')
    url: str = Field(default='Unknown')


class Settings(BaseSettings):
    discord: Dict[str, DiscordTopic] = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_prefix='COMMON_',
        env_file_encoding='utf-8',
        env_file=(f'.env.{env}'),
        extra='ignore'
    )


# DB Connection을 위한 신규 Settings 추가
class DBSettings(BaseSettings):
    host: str = Field(default='None')
    port: int = Field(default=-99)
    name: str = Field(default='None')
    user: str = Field(default='None')
    pw: str = Field(default='None')

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file_encoding='utf-8',
        env_file=(f'.env.{env}'),
        extra='ignore'
    )


settings = Settings(_env_file_encoding='utf-8')
db_settings = DBSettings(_env_file_encoding='utf-8')


def get_topic(name: str) -> DiscordTopic:
    try:
        return settings.discord[name]
    except KeyError:
        raise KeyError(f'Discord topic {name} is not defined in the settings')
    

def get_db_config() -> DBSettings:
    try:
        return db_settings
    except KeyError:
        raise KeyError(f"Database configuration is not defined in the settings")