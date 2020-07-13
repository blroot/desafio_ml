from flask import current_app as app
from filereader.parsers import StreamParserFactory
from record.Record import Record
from typing import Type
import os


class FileReader:
    def __init__(self, parser_factory: StreamParserFactory, record_format: Type[Record], file_name: str):
        self.file_name = file_name
        self.file_path = app.config.get("FILE_PATH")
        self.parser = parser_factory.get_parser(app.config.get("FILE_TYPE"))
        self.record_format = record_format

    def read_line(self):
        with open(self.file_path + self.file_name, "r") as f:
            reader = self.parser.reader(f)
            for row in reader:
                yield self.parser.build_record(row, self.record_format)

    def remove_file(self):
        os.remove(self.file_path + self.file_name)
