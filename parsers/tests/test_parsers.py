from parsers.JsonLinesParser import JsonLinesParser
import unittest


class JsonLinesParserTest(unittest.TestCase):
    def test_jsonlines_parser_returns_a_dict(self):
        with open('parsers/tests/files/example.jsonl') as f:
            parser = JsonLinesParser()
            for row in parser.reader(f):
                self.assertIsInstance(row, dict)

    def test_first_row_is_equal_to(self):
        with open('parsers/tests/files/example.jsonl') as f:
            parser = JsonLinesParser()
            second_row = next(parser.reader(f))
            self.assertDictEqual(second_row, {"name": "Gilbert", "wins": [["straight", "7♣"], ["one pair", "10♥"]]})


if __name__ == '__main__':
    unittest.main()
