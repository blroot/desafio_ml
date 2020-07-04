class StreamParserFactory:
    def __init__(self):
        self._parsers = {}

    def register_parser(self, type_format, parser):
        self._parsers[type_format] = parser

    def get_parser(self, type_format):
        return self._parsers.get(type_format)
