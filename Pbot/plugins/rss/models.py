from Pbot.db import db


class Rss(db.Model):
    __tablename__ = "rss"

    id = db.Column(db.String(20), primary_key=True)
    dt = db.Column(db.String(100))
    owner = db.Column(
        db.String(20),
        nullable=False,
        server_default=db.text("'sys'::character varying"),
    )
    pre = db.Column(db.String(50))


class Sub(db.Model):
    __tablename__ = "subs"

    qid = db.Column(db.BigInteger, primary_key=True, nullable=False)
    dt = db.Column(db.String(100), nullable=False)
    rss = db.Column(
        db.ForeignKey("rss.id"), primary_key=True, nullable=False, index=True
    )
