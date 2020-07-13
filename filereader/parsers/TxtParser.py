from filereader.parsers.Parser import Parser


class TxtParser(Parser):
    def __init__(self, delimiter=" "):
        self._delimiter = delimiter

    def reader(self, file_object):
        for line in file_object:
            yield line.rstrip().split(self._delimiter)
