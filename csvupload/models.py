from . import db


class SiteIdPriceStartTimeNameDescriptionNickname(db.Model):
    __tablename__ = 'a_table'
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
