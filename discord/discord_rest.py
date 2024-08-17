import logging

from typing import Optional, Dict, List, Any
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
            connector=TCPConnector(ssl=False),
            timeout=ClientTimeout(3),
        )

    async def execute(self, url: str, embed: DiscordEmbed) -> None:
        json = {
            "content": "Hello World",
            "embeds": [asdict(embed)],
        }

        async with self._client.post(url, json=json) as response:
            if response.status != 204:
                logger.error(f"Failed to execute webhook: {response.status}")
                raise Exception(f"Failed to execute webhook: {response.status}")