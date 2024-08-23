import pytest

from common.discord.discord_rest import DiscordRest, DiscordEmbed


@pytest.mark.asyncio
async def test_execute():
    web_hook_url = 'https://discord.com/api/webhooks/1274381556315852882/wyhFO7Xys5JlSi0Gypm9FppyGI_SstKXJcJ4rLLPoYP1VrcTsw-6hwTqMUAKeyuC2y5E'
    rest = DiscordRest()
    embed = DiscordEmbed(
        author={"name": "name"},
        title="title",
        fields=[{"name": "name", "value": "value"}],
        color=0x00FF00
    )

    await rest.execute(web_hook_url, embed)
