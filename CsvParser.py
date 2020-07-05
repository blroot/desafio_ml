import csv


class CsvParser:
    def reader(self, file_object):
        reader = csv.reader(file_object)
        next(reader)
        return reader

    def build_record(self, values, record_class):
        return record_class(values)
