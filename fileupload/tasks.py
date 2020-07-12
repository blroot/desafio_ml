from fileupload import celery
import datetime
from record.RecordPool import RecordPool
from fileupload.models import db, UploadStatus
from filereader.FileReader import FileReader
from fileupload import parser_factory
from record.SiteIdPriceStartTimeNameDescriptionNicknameRecord import SiteIdPriceStartTimeNameDescriptionNicknameRecord
from HTTPApi.MLApi import MLApi


@celery.task()
def bg_task(upload_id, file_name):
    ml_api = MLApi("https://api.mercadolibre.com")
    upload_status = db.session.query(UploadStatus).filter(UploadStatus.id == upload_id).one()

    file_reader = FileReader(parser_factory, SiteIdPriceStartTimeNameDescriptionNicknameRecord, file_name)

    start_time = datetime.datetime.now()

    record_pool = RecordPool(ml_api=ml_api)
    for db_record in file_reader.read_line():
        db_record.load_stages()
        record_pool.records.append(db_record)

    upload_status.status = 'running'
    db.session.commit()

    record_pool.run_all_pipelines()

    record_pool.save_all_records()

    end_time = datetime.datetime.now()

    upload_status.status = 'done'
    upload_status.time_elapsed = (end_time-start_time).total_seconds()
    db.session.commit()

    file_reader.remove_file()
