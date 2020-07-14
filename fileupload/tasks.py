from fileupload import celery
from fileupload.SiteIdPriceStartTimeNameDescriptionNicknameRecord import SiteIdPriceStartTimeNameDescriptionNicknameRecord
import datetime
from flask import current_app as app
from filereader.record.RecordPool import RecordPool
from fileupload.models import db, UploadStatus
from filereader.FileReader import FileReader
from fileupload import parser_factory
from HTTPApi.MLApi import MLApi
from HTTPApi.Exceptions import ApiConnectionError


@celery.task()
def bg_task(upload_id: int, file_name: str):
    ml_api = MLApi("https://api.mercadolibre.com", app.config.get("ASYNC_REQUESTS_SEMAPHORE"))
    upload_status = db.session.query(UploadStatus).filter(UploadStatus.id == upload_id).one()

    file_reader = FileReader(parser_factory, SiteIdPriceStartTimeNameDescriptionNicknameRecord, file_name)

    start_time = datetime.datetime.now()

    upload_status.status = 'running'
    db.session.commit()

    record_pool = RecordPool(ml_api=ml_api, size=app.config.get("RECORD_POOL_SIZE"))
    try:
        record_pool.main_loop(file_reader)
    except ApiConnectionError as e:
        upload_status.status = 'failed'
        upload_status.details = str(e)
        db.session.commit()
        file_reader.remove_file()
        return

    end_time = datetime.datetime.now()

    upload_status.status = 'done'
    upload_status.time_elapsed = (end_time-start_time).total_seconds()
    db.session.commit()

    file_reader.remove_file()
