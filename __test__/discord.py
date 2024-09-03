import asyncio
from common.discord import notify, notify_info, DiscordMessage, MessageColor


async def main():
    message = DiscordMessage(
        topic='sample_topic',
        title='title',
        message='message',
        data={'key': 'value'}
    )

    await notify(message, color=MessageColor.INFO)
    await notify_info(message)


if __name__ == '__main__':
    asyncio.run(main())
