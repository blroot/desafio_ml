from filereader.parsers.Parser import Parser
import json


class JsonLinesParser(Parser):
    def reader(self, file_object):
        for line in file_object:
            yield json.loads(line)
