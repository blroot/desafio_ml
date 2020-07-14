from filereader.parsers.Parser import Parser
from typing import TextIO
import csv


class CsvParser(Parser):
    def __init__(self, delimiter=","):
        self._delimiter = delimiter

    def reader(self, file_object: TextIO):
        """
        Método que adapta el generador de csv.reader para leer linea a linea
        :param file_object: El objeto file
        :return: csv.reader
        """
        reader = csv.reader(file_object, delimiter=self._delimiter)
        next(reader)
        return reader
