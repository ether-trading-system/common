import os

from discord.settings import settings


def test_env():
    env = os.environ.get("ENV", "")
    print(f'.env.{env}')
    assert env == "test"


def test_env_value():
    service_name = "APPLE"
    common = "COMMON"
    assert settings.service_name == service_name
    assert settings.common == common
