from flask import Flask, request, Response
from FileReader import FileReader
from StreamParserFactory import StreamParserFactory
import csv
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
parser_factory = StreamParserFactory()
parser_factory.register_parser('csv', csv.reader)


@app.route('/desafioml', methods=["POST"])
def upload() -> str:
    file_reader = FileReader(config, parser_factory)
    file_reader.upload(request)
    return Response(None, status=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
