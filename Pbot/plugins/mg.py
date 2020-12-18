from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.permission import SUPERUSER
from Pbot.db import Mg

on = on_command("on", priority=1)
off = on_command("off", priority=1)
mg = on_command("mg", priority=1)
grant = on_command("grant", priority=1)
cmd = {
    "safe": "安全模式",
    "rss": "群内 rss 通知",
    "white": "是否相应本群消息",
    "ghz": "公会战模式",
    "morningcall": "早安！",
}


@on.handle()
async def on_func(bot: Bot, event: Event, state: dict):
    msg = await swcmd(bot, event, True)
    await on.send(msg)


@off.handle()
async def off_func(bot: Bot, event: Event, state: dict):
    msg = await swcmd(bot, event, False)
    await off.send(msg)


@grant.handle()
async def grant_func(bot: Bot, event: Event, state: dict):
    a = event.plain_text.strip().split()
    for i in a:
        await Mg.create(gid=int(i), white=True)

    await grant.send("已给群「{}」基础版授权。".format(" 、".join(a)))


async def swcmd(bot: Bot, event: Event, on: bool):
    if event.detail_type == "private":
        return "目前仅支持针对群聊的操控哦！"
    ccmd = event.plain_text.strip().split(" ")
    ans = []
    value = await Mg.query.where(Mg.gid == event.group_id).gino.first()
    if value == None:
        value = await Mg.create(gid=event.group_id, white=True)
    for i in ccmd:
        if i in cmd:
            kwargs={i: on}
            await value.update(**kwargs).apply()
            ans.append(cmd[i])
    if len(ans) > 0:
        return "{} 功能已{}".format("、".join(ans), "开启" if on else "关闭")
