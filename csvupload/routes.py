from flask import request, Response, jsonify
from flask import current_app as app
from FileReader import FileReader
from StreamParserFactory import StreamParserFactory
from file_record.SiteAndIdRecord import SiteAndIdRecord
from db_record.SiteIdPriceStartTimeNameDescriptionNicknameRecord import SiteIdPriceStartTimeNameDescriptionNicknameRecord
from RecordPool import RecordPool
from CsvParser import CsvParser
import configparser
import datetime
from HTTPApi.MLApi import MLApi

config = configparser.ConfigParser()
parser_factory = StreamParserFactory()
parser_factory.register_parser('csv', CsvParser)


@app.route('/desafioml', methods=["POST"])
def upload() -> str:
    ml_api = MLApi("https://api.mercadolibre.com")
    start_time = datetime.datetime.now()
    file_reader = FileReader(parser_factory, SiteAndIdRecord)
    file_reader.upload(request)
    record_pool = RecordPool(ml_api=ml_api)
    for file_record in file_reader.read_line():
        db_record = SiteIdPriceStartTimeNameDescriptionNicknameRecord(file_record)
        db_record.load_stages()
        record_pool.records.append(db_record)
    record_pool.run_all_pipelines()
    record_pool.save_all_records()
    end_time = datetime.datetime.now()
    return jsonify({"time": str((end_time-start_time).total_seconds())})
