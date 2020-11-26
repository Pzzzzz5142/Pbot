from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_regex
from Pbot.utils import cksafe, getImage, getSetuHigh
import Pbot.cq as cq

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

    pic, data = await getSetuHigh(bot, r18)
    if isinstance(data, str):
        text = data
    else:
        text = """发送中，。，。，。\npixiv id:{}\ntitle:{}\n作者:{}\ntags:{}""".format(
            data["pid"],
            data["title"],
            data["author"],
            "、".join(["#" + i for i in data["tags"]]),
        )
    await setu.send(
        text, at_sender=True,
    )
    try:
        await setu.send(pic)
    except:
        pass
