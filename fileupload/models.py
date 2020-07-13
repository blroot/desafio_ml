from . import db


class UploadStatus(db.Model):
    __tablename__ = 'upload_status'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    status = db.Column(
        db.String(10),
        index=False,
        unique=False,
    )
    details = db.Column(
        db.String(100),
        index=False,
        unique=False,
    )
    time_elapsed = db.Column(
        db.Float,
        primary_key=False,
        default=0.0
    )


class SiteIdPriceStartTimeNameDescriptionNickname(db.Model):
    __tablename__ = 'data'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    site = db.Column(
        db.String(3),
        index=False,
        unique=False,
    )
    item_id = db.Column(
        db.Integer,
        index=False,
        unique=False,
    )
    price = db.Column(
        db.Float,
        primary_key=False,
    )
    start_time = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    name = db.Column(
        db.String(50),
        index=False,
        unique=False,
    )
    description = db.Column(
        db.String(50),
        index=False,
        unique=False,
    )
    nickname = db.Column(
        db.String(50),
        index=False,
        unique=False,
    )
