from filereader.parsers.JsonLinesParser import JsonLinesParser
from filereader.parsers.CsvParser import CsvParser
from filereader.parsers.TxtParser import TxtParser
import unittest


class JsonLinesParserTest(unittest.TestCase):
    def test_jsonlines_parser_returns_a_dict(self):
        with open('filereader/tests/files/example.jsonl') as f:
            parser = JsonLinesParser()
            for row in parser.reader(f):
                self.assertIsInstance(row, dict)

    def test_first_row_is_equal_to(self):
        with open('filereader/tests/files/example.jsonl') as f:
            parser = JsonLinesParser()
            first_row = next(parser.reader(f))
            self.assertDictEqual(first_row, {"name": "Gilbert", "wins": [["straight", "7♣"], ["one pair", "10♥"]]})


class CsvParserTest(unittest.TestCase):
    def test_csv_parser_returns_a_list(self):
        with open('filereader/tests/files/example.csv') as f:
            parser = CsvParser()
            for row in parser.reader(f):
                self.assertIsInstance(row, list)

    def test_first_row_is_equal_to(self):
        with open('filereader/tests/files/example.csv') as f:
            parser = CsvParser()
            first_row = next(parser.reader(f))
            self.assertListEqual(first_row, ['MLA', '750925229'])


class TxtParserTest(unittest.TestCase):
    def test_txt_parser_returns_a_list(self):
        with open('filereader/tests/files/example.txt') as f:
            parser = CsvParser()
            for row in parser.reader(f):
                self.assertIsInstance(row, list)

    def test_second_value_on_first_row_is_equal_to(self):
        with open('filereader/tests/files/example.txt') as f:
            parser = TxtParser()
            first_row = next(parser.reader(f))
            self.assertEqual(first_row[1], 'is')


if __name__ == '__main__':
    unittest.main()
