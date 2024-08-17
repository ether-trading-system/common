import os

from _pytest.python_api import raises
from discord.settings import get_topic


def test_env():
    env = os.environ.get("ENV", "")
    print(f'.env.{env}')
    assert env == "test"


def test_get_topic():
    with raises(KeyError) as error_info:
        get_topic('error_topic')

    assert error_info.value.args[0] == "Discord topic error_topic is not defined in the settings"
