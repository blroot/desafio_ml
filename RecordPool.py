from typing import Iterable, Coroutine
from flask import current_app as app
import asyncio
import aiohttp


class RecordPool:
    def __init__(self, ml_api=None):
        self.records = []
        self._ml_api = ml_api

    def run_all_pipelines(self):
        all_coroutines = []
        number_of_stages = len(self.records[0].tasks_pipeline)

        for i in range(number_of_stages):
            for record in self.records:
                task = record.tasks_pipeline[i]
                if record.continue_pipeline:
                    record_coroutines = task(self._ml_api)
                    if record.continue_pipeline:
                        all_coroutines += record_coroutines
            asyncio.run(self.request_aio(all_coroutines))
            all_coroutines = []
        for record in self.records:
            if record.continue_pipeline:
                record.end_pipeline(self._ml_api)

    async def request_aio(self, endpoints: Iterable[Coroutine]) -> None:
        sem = asyncio.Semaphore(app.config.get("ASYNC_REQUESTS_SEMAPHORE"))
        sem_items = asyncio.Semaphore(1)

        async def request(endpoint, s) -> None:
            cr, item_id = endpoint
            await sem.acquire()
            await cr(s, item_id=item_id, semaphore=sem_items)
            sem.release()

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[request(endpoint, session) for endpoint in endpoints])

    def save_all_records(self):
        for record in self.records:
            if record.continue_pipeline:
                record.save()
