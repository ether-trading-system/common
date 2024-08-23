import asyncio
import logging
from functools import lru_cache
from types import TracebackType

from typing import Optional, Dict, List, Any, Type
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class DiscordEmbed:
    """
    https://discord.com/developers/docs/resources/webhook#execute-webhook-jsonform-params
    """
    author: Optional[Dict[str, Optional[str]]]
    color: Optional[int] = None
    fields: List[Dict[str, Optional[Any]]] = None
    title: Optional[str] = None
    # description: Optional[str] = None
    # footer: Optional[Dict[str, Optional[str]]] = None
    # image: Optional[Dict[str, Optional[Union[str, int]]]] = None
    # provider: Optional[Dict[str, Any]] = None
    # thumbnail: Optional[Dict[str, Optional[Union[str, int]]]] = None
    # timestamp: Optional[str] = None
    # url: Optional[str] = None
    # video: Optional[Dict[str, Optional[Union[str, int]]]] = None


class DiscordRest:
    _client: ClientSession

    def __init__(self):
        self._client = ClientSession(
            headers={"Content-Type": "application/json"},
            connector=TCPConnector(ssl=False, limit=30),
            timeout=ClientTimeout(3),
            loop=asyncio.get_event_loop(),
        )

    async def __aenter__(self) -> "DiscordRest":
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        # await self._client.close()
        pass

    async def execute(self, url: str, embed: DiscordEmbed) -> None:
        json = {
            "embeds": [asdict(embed)],
        }

        async with self._client.post(url, json=json) as response:
            if response.status != 204:
                logger.error(f"Failed to execute webhook: {response.status}")
                raise Exception(f"Failed to execute webhook: {response.status}")


@lru_cache
def get_discord_rest():
    return DiscordRest()
