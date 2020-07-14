import asyncio
from HTTPApi.MLApi import MLApi


class RecordPool:
    def __init__(self, ml_api: MLApi, size: int):
        self.records = []
        self._ml_api = ml_api
        self.size = size

    def main_loop(self, file_reader):
        """
        Es el loop principal del sistema, carga N (size) records al pool, para cada uno corre su pipeline,
        guarda los datos y purga caches

        :param file_reader: Instancia de FileReader
        """
        file_reader_generator = file_reader.read_line()
        while True:
            try:
                chunk = [next(file_reader_generator) for _ in range(self.size)]
                self.records.extend(chunk)
                self._run_all_pipelines()
                self._save_all_records()
                self._ml_api.purge_all_caches()
            except StopIteration:
                break

    def _run_all_pipelines(self):
        """
        Se usa de forma privada para manejar las corrutinas,
        con el resultado de las etapas indicadas en el record encola y corre las tareas
        asincrónicas.
        """
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

    def _save_all_records(self):
        """
        Salva todos los records en DB y vacía caches de los Endpoints
        """
        for record in self.records:
            if record.continue_pipeline:
                record.save()
        self.records = []

