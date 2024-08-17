import os

from typing import Dict
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.environ.get("ENV", "")


class DiscordTopic(BaseModel):
    name: str = Field(default='Unknown')
    url: str = Field(default='Unknown')


class Settings(BaseSettings):
    discord: Dict[str, DiscordTopic] = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_prefix='COMMON_',
        env_file_encoding='utf-8',
        env_file=('.env', f'.env.{env}'),
        extra='ignore'
    )


settings = Settings(_env_file_encoding='utf-8')


def get_topic(name: str) -> DiscordTopic:
    try:
        return settings.discord[name]
    except KeyError:
        raise KeyError(f'Discord topic {name} is not defined in the settings')
