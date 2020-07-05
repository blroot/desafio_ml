from .FileRecord import FileRecord


class SiteAndIdRecord(FileRecord):
    def render(self):
        return self.values[0] + str(self.values[1])

    def transform(self):
        if self.values[0] not in ['MLB', 'MLA']:
            return False
        try:
            self.values[1] = int(self.values[1])
        except ValueError:
            return False

        return True
