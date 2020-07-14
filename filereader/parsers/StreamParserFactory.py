from typing import Type
from filereader.parsers.Parser import Parser


class StreamParserFactory:
    def __init__(self, delimiter=","):
        self._parsers = {}
        self._delimiter = delimiter

    def register_parser(self, type_format: str, parser: Type[Parser]):
        """
        Permite registrar un Parser asociado a una extensión determinada
        :param type_format: Extensión de archivo
        :param parser: Clase correspondiente al Parser
        """
        self._parsers[type_format] = parser

    def get_parser(self, type_format: str):
        """
        Devuelve un objeto parser construído
        :param type_format: Extensión de archivo
        :return: Objeto Parser
        """
        return self._parsers.get(type_format)(delimiter=self._delimiter)
