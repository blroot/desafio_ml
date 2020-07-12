from flask import request, jsonify, abort
from flask import current_app as app
from fileupload.models import db, UploadStatus
from sqlalchemy.orm.exc import NoResultFound
from .tasks import bg_task
import string
import random


@app.route('/uploadfile', methods=["POST"])
def upload() -> str:
    file = request.files['file']
    file_name = ''.join(random.choice(string.ascii_letters) for i in range(10))
    file_path = app.config.get("FILE_PATH")

    file.save(file_path + file_name)

    new_upload_status = UploadStatus(status='uploaded')
    db.session.add(new_upload_status)
    db.session.commit()

    bg_task.delay(new_upload_status.id, file_name)

    return jsonify({"upload_id": new_upload_status.id})


@app.route('/uploadstatus/<int:upload_id>', methods=["GET"])
def status(upload_id) -> str:
    try:
        upload_status = db.session.query(UploadStatus).filter(UploadStatus.id == upload_id).one()
        return jsonify({"id": upload_id, "status": upload_status.status, "time_elapsed": upload_status.time_elapsed})
    except NoResultFound:
        abort(404)
