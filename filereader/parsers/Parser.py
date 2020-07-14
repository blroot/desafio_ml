from typing import TextIO, Type
from filereader.record.Record import Record


class Parser:
    def reader(self, file_object: TextIO):
        """
        Método base para implementar un generador para leer una linea a la vez

        :param file_object: None
        """
        pass

    @staticmethod
    def build_record(values, record_class: Type[Record]):
        """
        Se utiliza para construír un objeto Record

        :param values: La estructura de datos que devuelve el parser
        :param record_class: Una clase hija de Record
        :return: Un objeto hijo de la clase Record
        """
        return record_class(values)
