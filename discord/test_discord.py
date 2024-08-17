import asyncio

import pytest

from discord import notify, DiscordMessage, notify_danger, notify_success, notify_info, notify_warning, MessageColor


@pytest.mark.asyncio
async def test_notify():
    # Arrange
    message = DiscordMessage(
        topic='sample_topic',
        title='title',
        message='message',
        data={'key': 'value'}
    )

    # Act
    await asyncio.gather(*[
        notify(message, color=MessageColor.INFO),
        notify_danger(message),
        notify_success(message),
        notify_info(message),
        notify_warning(message)
    ])
