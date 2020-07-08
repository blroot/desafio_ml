class DBRecord:
    def __init__(self, file_record):
        self.file_record = file_record
        self.transform_success = False
        self.tasks_pipeline = ()

    def save(self):
        pass

    def load_stages(self):
        pass

    def end_pipeline(self, ml_api):
        pass
