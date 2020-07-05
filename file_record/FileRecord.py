class FileRecord:
    def __init__(self, values):
        self.values = values

    def transform(self):
        return True

    def render(self):
        return self.values
