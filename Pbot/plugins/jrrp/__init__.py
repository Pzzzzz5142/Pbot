from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
import datetime
import random
import Pbot.cq as cq
from .models import Jrrp

jrrp = on_command("jrrp")


@jrrp.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    today = datetime.date.today()
    ans = -1
    random.seed(datetime.datetime.now())
    value = await Jrrp.query.where(Jrrp.qid == event.user_id).gino.first()
    if value == None:
        value = await Jrrp.create(qid=event.user_id)
    ans = value.rand
    if value.dt != today:
        ans = random.randint(0, 100)
        await value.update(dt=today, rand=ans).apply()

    await jrrp.finish(unescape(cq.at(event.user_id) + "今天的人品为：{} 哦！".format(ans)))
