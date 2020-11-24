from Pbot.db import db


class Jrrp(db.Model):
    __tablename__ = "jrrp"

    qid = db.Column(db.BigInteger, primary_key=True)
    dt = db.Column(db.Date)
    rand = db.Column(db.Integer)
