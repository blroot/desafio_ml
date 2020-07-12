class Parser:
    def reader(self, file_object):
        pass

    @staticmethod
    def build_record(values, record_class):
        return record_class(values)
