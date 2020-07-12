from filereader.parsers.Parser import Parser


class TxtParser(Parser):
    def reader(self, file_object):
        for line in file_object:
            yield line.rstrip().split(" ")
