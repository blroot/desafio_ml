from typing import Iterable, Coroutine
from flask import current_app as app
import asyncio
import aiohttp


class RecordPool:
    def __init__(self, ml_api=None):
        self.records = []
        self._ml_api = ml_api

    def run_all_pre_transforms(self):
        all_coroutines = []

        for record in self.records:
            record.transform_success, record_coroutines = record.pre_transform(self._ml_api)
            all_coroutines += record_coroutines
        asyncio.run(self.request_aio(all_coroutines))

    def run_all_transforms(self):
        all_coroutines = []

        for record in self.records:
            record.transform_success, record_coroutines = record.transform(self._ml_api)
            all_coroutines += record_coroutines
        asyncio.run(self.request_aio(all_coroutines))
        for record in self.records:
            if record.transform_success:
                record.resolve_async(self._ml_api)

    async def request_aio(self, endpoints: Iterable[Coroutine]) -> None:
        sem = asyncio.Semaphore(app.config.get("ASYNC_REQUESTS_SEMAPHORE"))

        async def request(endpoint, s) -> None:
            cr, item_id, cache = endpoint
            await sem.acquire()
            await cr(s, item_id=item_id, cache=cache)
            sem.release()

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[request(endpoint, session) for endpoint in endpoints])

    def save_all_records(self):
        for record in self.records:
            if record.transform_success:
                record.save()
