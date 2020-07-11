import csv


class CsvParser:
    def __init__(self, delimiter=","):
        self._delimiter = delimiter

    def reader(self, file_object):
        reader = csv.reader(file_object, delimiter=self._delimiter)
        next(reader)
        return reader

    @staticmethod
    def build_record(values, record_class):
        return record_class(values)
