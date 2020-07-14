class Record:
    def __init__(self, values):
        self.values = values
        self.continue_pipeline = True
        self.tasks_pipeline = ()

    def end_pipeline(self, ml_api):
        """
        Implementar, anteúltima etapa del pipeline, donde se pueden consultar datos a caché

        :param ml_api: Instancia de MLApi
        """
        pass

    def save(self):
        """
        Tiene que implementarse para salvar los datos en BD. Última etapa del pipeline
        """
        pass

    def cancel_pipeline(self):
        """
        Llamar si se necesita interrumpir la ejecución del pipeline
        """
        self.continue_pipeline = False
