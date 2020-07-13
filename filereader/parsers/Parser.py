from typing import TextIO, Type
from record.Record import Record


class Parser:
    def reader(self, file_object: TextIO):
        pass

    @staticmethod
    def build_record(values, record_class: Type[Record]):
        return record_class(values)
