from filereader.parsers.Parser import Parser
from typing import TextIO
import json


class JsonLinesParser(Parser):
    def reader(self, file_object: TextIO):
        for line in file_object:
            yield json.loads(line)
