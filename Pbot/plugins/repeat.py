from nonebot import on_message
from math import exp
from random import random
from nonebot.adapters.cqhttp import Bot, Event

repeat = on_message(priority=5)

tjmp = {}


def sigmoid(num):
    num //= 2
    if num < 1:
        return -1
    num -= 3
    print(1 / (1 + exp(-num)))
    return 1 / (1 + exp(-num))


@repeat.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    global tjmp
    if event.detail_type != "group":
        return
    if event.group_id not in tjmp:
        tjmp[event.group_id] = [0, "", "", 0]
    now = tjmp[event.group_id]
    try:
        if msg == now[2]:
            now[0] += 1
        if "pixiv" in msg and "rss " in msg and "r18" in msg:
            now[-1] += 1
        else:
            now[-1] = 0
            raise Exception
        if now[-1] > 3:
            # await call_command(session.bot, event, "怜悯")
            now[-1] = 0
            raise Exception
    except:
        pass
    if msg == "" or msg == now[1] or msg != now[2]:
        now[0] = 1
        now[2] = msg
        return
    now[2] = msg
    if random() < sigmoid(now[0]):
        now[1] = msg
        await repeat.send(msg)
        now[0] = 0
        return
