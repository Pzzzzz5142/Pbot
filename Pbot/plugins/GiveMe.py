from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.rule import regex
from Pbot.utils import cksafe
import Pbot.cq as cq

setu = on_command("来份涩图", rule=regex("^来.*份.*(涩|色)图"))


@setu.handle()
async def sst(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    api = r"https://api.lolicon.app/setu/"
    parm = {"apikey": bot.config.LoliAPI, "r18": "1", "size1200": "true"}
    if event.detail_type == "group":
        safe = await cksafe(event.group_id)
    else:
        safe = False
    if ("r18" in msg or "R18" in msg) and not safe:
        parm["r18"] = 1
    else:
        parm["r18"] = 0
    async with bot.config.session.get(api, params=parm) as resp:
        if resp.status != 200:
            await setu.finish("网络错误：" + str(resp.status))
        ShitJson = await resp.json()
        if ShitJson["quota"] == 0:
            await setu.finish(
                f"返回码：{ShitJson['code']}\napi调用额度已耗尽，距离下一次调用额度恢复还剩 {ShitJson['quota_min_ttl']+1} 秒。"
            )
        data = ShitJson["data"][0]
        await setu.send(
            """发送中，。，。，。\npixiv id:{}\ntitle:{}\n作者:{}\ntgas:{}""".format(
                data["pid"],
                data["title"],
                data["author"],
                "、".join(["#" + i for i in data["tags"]]),
            ),
            at_sender=True,
        )
        await setu.send(cq.image(ShitJson["data"][0]["url"]))
