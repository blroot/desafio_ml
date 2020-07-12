from filereader.parsers.Parser import Parser
import csv


class CsvParser(Parser):
    def __init__(self, delimiter=","):
        self._delimiter = delimiter

    def reader(self, file_object):
        reader = csv.reader(file_object, delimiter=self._delimiter)
        next(reader)
        return reader
