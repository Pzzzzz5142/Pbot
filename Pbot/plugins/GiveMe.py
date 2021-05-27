import re
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.plugin import on_command, on_message, on_regex
from Pbot.utils import cksafe, getSetuHigh
from Pbot.rule import ckimg
import Pbot.cq as cq
from datetime import datetime

setu = on_regex("^来.*份.*(涩|色)图")


@setu.handle()
async def sst(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    if event.detail_type == "group":
        safe = await cksafe(event.group_id)
    else:
        safe = False
    if ("r18" in msg or "R18" in msg) and not safe:
        r18 = True
    else:
        r18 = False

    msg = re.sub("(r|R)18", "", msg)
    fd = re.search("份.*(涩|色)", msg)
    try:
        keyword = msg[fd.start() + 1 : fd.end() - 1]
    except:
        keyword = ""

    pic, data = await getSetuHigh(bot, r18, keyword)
    if isinstance(data, str):
        text = data
    else:
        text = """发送中，。，。，。\npixiv id:{}\ntitle:{}\n作者:{}\ntags:{}""".format(
            data["pid"], data["title"], data["author"], "、".join(data["tags"])
        )
    try:
        await setu.send(
            text,
            at_sender=True,
        )
    except:
        try:
            await setu.send("呀，发送色图详情失败辣，。，")
        except:
            pass
    try:
        if pic != None:
            await setu.send(pic)
    except:
        await setu.send("呀，发送失败辣，。，")


act = on_command("act", priority=1)


@act.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    await act.finish(unescape(cq.image("activity.jpg")))


stCome = on_message(rule=ckimg("b407f708a2c6a506342098df7cac4a57.image"))


@stCome.handle()
async def pre(bot: Bot, event: Event, state: dict):
    if event.detail_type == "group":
        safe = await cksafe(event.group_id)
    else:
        safe = False
    x, err = await getSetuHigh(bot, not safe)
    if x == None:
        await stCome.finish(err)
    try:
        await stCome.send(unescape(x))
    except:
        await stCome.send("呀，发送失败辣，。，")
