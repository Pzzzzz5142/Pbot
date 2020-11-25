from nonebot import on_command
import nonebot
from nonebot.rule import startswith
from nonebot.adapters.cqhttp import Bot, Event
import Pbot.cq as cq, json

dg = on_command("点歌", rule=startswith("点歌"))

parm = {"type": "1", "s": "十年", "limit": 1}


@dg.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    if msg == "":
        dg.finish("参数为空！！！")
    parm["s"] = msg
    async with bot.config.session.get(
        "https://music.163.com/api/search/get/web", params=parm
    ) as resp:
        if resp.status != 200:
            dg.finish("网络错误哦，咕噜灵波～(∠・ω< )⌒★")
        ShitJson = await resp.read()
        ShitJson = json.loads(ShitJson)
        ShitJson = ShitJson["result"]["songs"][0]["id"]
        await dg.send(
            cq.music("163", ShitJson), auto_escape=False,
        )
