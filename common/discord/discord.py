import json
import asyncio
import logging

from typing import Dict, Any, Optional, List
from common.discord.message_color import MessageColor
from common.settings import get_topic
from fastapi import HTTPException
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


@dataclass
class DiscordMessage:
    topic: str
    title: str
    message: str
    data: Optional[Dict[str, Any]]


async def execute(url: str, embed: DiscordEmbed) -> None:
    json = {
        "embeds": [asdict(embed)],
    }

    async with ClientSession(
            headers={"Content-Type": "application/json"},
            connector=TCPConnector(ssl=False, limit=30),
            timeout=ClientTimeout(3),
            loop=asyncio.get_event_loop(),
    ) as session:
        async with session.post(url, json=json) as response:
            if response.status != 204:
                logger.error(f"Failed to execute webhook: {response.status}")
                raise Exception(f"Failed to execute webhook: {response.status}")


async def notify(message: DiscordMessage, color: MessageColor) -> None:
    topic = get_topic(message.topic)
    embed = DiscordEmbed(
        author={"name": topic.name},
        title=message.title,
        color=color.value,
        fields=[*map(lambda x: {"name": x,
                                "value": f"```json\n{json.dumps(message.data[x], indent=4, ensure_ascii=False)}\n```"},
                     message.data)]
    )
    await execute(topic.url, embed)


async def notify_danger(message: DiscordMessage) -> None:
    await notify(message, MessageColor.DANGER)


async def notify_warning(message: DiscordMessage) -> None:
    await notify(message, MessageColor.WARNING)


async def notify_info(message: DiscordMessage) -> None:
    await notify(message, MessageColor.INFO)


async def notify_success(message: DiscordMessage) -> None:
    await notify(message, MessageColor.SUCCESS)


async def notify_error(exception: HTTPException, data: Optional[Dict[str, Any]]) -> None:
    message = DiscordMessage(topic="error", title=f"[{exception.name}] {exception.detail}", message="", data=data)
    await notify_danger(message)
