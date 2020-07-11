class Record:
    def __init__(self, values):
        self.values = values
        self.continue_pipeline = True
        self.tasks_pipeline = ()

    def save(self):
        pass

    def load_stages(self):
        pass

    def end_pipeline(self, ml_api):
        pass

    def cancel_pipeline(self):
        self.continue_pipeline = False
