from Pbot.db import db


class MusicPoll(db.Model):
    __tablename__ = "music_poll"

    id = db.Column(db.BigInteger, primary_key=True)
    result = db.Column(db.Integer)
    div2 = db.Column(db.Integer)
    base_remi = db.Column(db.Integer)
    top5_div2 = db.Column(db.Integer)
    remi_cov = db.Column(db.Integer)
    comment = db.Column(db.CHAR(100))
    ind = db.Column(db.Integer, primary_key=True)
