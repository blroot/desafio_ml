from filereader.parsers.Parser import Parser
from typing import TextIO
import json


class JsonLinesParser(Parser):
    def reader(self, file_object: TextIO):
        """
        Generador, interpreta una linea como json
        :param file_object: El objeto file
        """
        for line in file_object:
            yield json.loads(line)
