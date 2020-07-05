from flask import request, Response
from flask import current_app as app
from FileReader import FileReader
from StreamParserFactory import StreamParserFactory
from file_record.SiteAndIdRecord import SiteAndIdRecord
from db_record.SiteIdPriceStartTimeNameDescriptionNicknameRecord import SiteIdPriceStartTimeNameDescriptionNicknameRecord
from CsvParser import CsvParser
import configparser
import datetime

config = configparser.ConfigParser()
parser_factory = StreamParserFactory()
parser_factory.register_parser('csv', CsvParser)


@app.route('/desafioml', methods=["POST"])
def upload() -> str:
    start_time = datetime.datetime.now()
    file_reader = FileReader(parser_factory, SiteAndIdRecord)
    file_reader.upload(request)
    for file_record in file_reader.read_line():
        db_record = SiteIdPriceStartTimeNameDescriptionNicknameRecord(file_record)
        if db_record.transform():
            db_record.save()
    end_time = datetime.datetime.now()
    return Response(str((end_time-start_time).total_seconds()), status=200)
