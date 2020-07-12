import asyncio


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
            asyncio.run(self._ml_api.request_aio(all_coroutines))
            all_coroutines = []
        for record in self.records:
            if record.continue_pipeline:
                record.end_pipeline(self._ml_api)

    def save_all_records(self):
        for record in self.records:
            if record.continue_pipeline:
                record.save()
