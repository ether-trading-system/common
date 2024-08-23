import json
from http import HTTPStatus

from typing import Dict, Any, Optional
from dataclasses import dataclass
from discord.discord_rest import DiscordEmbed, get_discord_rest
from discord.message_color import MessageColor
from discord.settings import get_topic
from fastapi import HTTPException



@dataclass
class DiscordMessage:
    topic: str
    title: str
    message: str
    data: Optional[Dict[str, Any]]


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
    async with get_discord_rest() as rest:
        await rest.execute(topic.url, embed)


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
