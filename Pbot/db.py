from gino import Gino
from nonebot.log import logger
import nonebot, aiohttp

db = Gino()


async def init() -> None:
    """
    Initialize database module.
    """
    config = nonebot.get_driver().config
    config.session = aiohttp.ClientSession()
    config = nonebot.get_driver().config
    logger.debug("Initializing database")
    if getattr(config, "db_dsn", None):
        await db.set_bind(config.db_dsn)
        logger.info("Database connected")
    else:
        logger.warning("DB_DSN is missing, database may not work")


class Acc(db.Model):
    __tablename__ = "acc"

    qid = db.Column(db.BigInteger, primary_key=True)
    money = db.Column(db.Float(53), nullable=False, server_default=db.text("1000000"))


class Backup(db.Model):
    __tablename__ = "backup"

    qid = db.Column(db.BigInteger, primary_key=True)
    card = db.Column(db.String(50))
    role = db.Column(db.String(10))


class Mg(db.Model):
    __tablename__ = "mg"

    gid = db.Column(db.BigInteger, primary_key=True)
    white = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))
    rss = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))
    safe = db.Column(db.Boolean, nullable=False, server_default=db.text("true"))
    ghz = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))
    morningcall = db.Column(db.Boolean, nullable=False, server_default=db.text("false"))


class Notebook(db.Model):
    __tablename__ = "notebook"

    qid = db.Column(db.BigInteger, primary_key=True, nullable=False)
    item = db.Column(db.String(200), primary_key=True, nullable=False)
    ind = db.Column(db.Integer)


class Quser(db.Model):
    __tablename__ = "quser"

    qid = db.Column(db.BigInteger, primary_key=True)
    swid = db.Column(db.CHAR(12))
    noteind = db.Column(db.Integer, nullable=False, server_default=db.text("0"))


class Datou(db.Model):
    __tablename__ = "datou"

    qid = db.Column(
        db.ForeignKey("quser.qid", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    price = db.Column(db.Integer)


class Hold(db.Model):
    __tablename__ = "holds"
    __table_args__ = (db.UniqueConstraint("qid", "stk"),)

    qid = db.Column(db.ForeignKey("acc.qid"), primary_key=True, nullable=False)
    stk = db.Column(db.String(10), primary_key=True, nullable=False)
    nums = db.Column(db.BigInteger, nullable=False)

