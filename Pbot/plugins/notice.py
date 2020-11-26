from nonebot import on_notice
from nonebot.adapters.cqhttp import Bot, Event, unescape
from Pbot.utils import getSetuHigh
from datetime import datetime
import Pbot.cq as cq

poke = on_notice()
helloNew = on_notice()


@poke.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    if event.sub_type == "poke" and event.raw_event["target_id"] == 3418961367:
        r18 = False
        if event.group_id == 145029700:
            hour = datetime.today().hour
            r18 = hour <= 7 or hour >= 22
        x, err = await getSetuHigh(bot, r18)
        if x == None:
            await poke.finish(err)
        try:
            await poke.send(unescape(x))
        except:
            await poke.send("呀，发送失败辣，。，")


@helloNew.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    if event.detail_type == "group_increase":
        await helloNew.send(unescape(cq.at(event.user_id) + " 欢迎新人入群👏！"))
        await bot.send_private_msg(user_id=545870222, message=f"新入群 {event.group_id}")
