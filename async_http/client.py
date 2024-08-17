class AsyncHttpClient:
    _client

    def __init__(self, loop=None, **kwargs):
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop, **kwargs)

    async def fetch(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as response:
            return await response.text()

    async def close(self):
        await self.session.close()