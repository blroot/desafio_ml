from HTTPApi.Endpoint import Endpoint
from HTTPApi.ItemsEndpoint import ItemsEndpoint
from typing import Iterable, Coroutine
import asyncio
import aiohttp


class MLApi:
    def __init__(self, url, async_limit):
        self.url = url
        self.items = ItemsEndpoint(url, 'items')
        self.currencies = Endpoint(url, 'currencies')
        self.categories = Endpoint(url, 'categories')
        self.users = Endpoint(url, 'users')
        self.async_limit = async_limit

    async def request_aio(self, endpoints: Iterable[Coroutine]) -> None:
        sem = asyncio.Semaphore(self.async_limit)

        async def request(endpoint, s) -> None:
            cr, item_id, extra_args = endpoint
            await sem.acquire()
            await cr(s, item_id=item_id, extra_args=extra_args)
            sem.release()

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[request(endpoint, session) for endpoint in endpoints])
