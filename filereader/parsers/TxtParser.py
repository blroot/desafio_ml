from filereader.parsers.Parser import Parser


class TxtParser(Parser):
    def __init__(self, delimiter=" "):
        self._delimiter = delimiter

    def reader(self, file_object):
        """
        Generador, remueve el salto de linea y separa el texto según el separador configurado

        :param file_object: El objeto file
        """
        for line in file_object:
            yield line.rstrip().split(self._delimiter)
