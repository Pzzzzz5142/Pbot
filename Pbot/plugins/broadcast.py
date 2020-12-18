from nonebot import on_command
from nonebot.message import handle_event
from nonebot.adapters.cqhttp import Bot, Event, Message
from nonebot.permission import SUPERUSER
import asyncio

bg = on_command("bg", permission=SUPERUSER, priority=1)


@bg.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    text = """！！！Bot维护通知！！！
可能的影响：
- bot不响应你的任何命令！
- st功能频繁出现403错误
"""

    reason = """
维护原因：

"""
    await bot.send_group_msg(group_id=1037557679, message="Halo")
    groups = await bot.get_group_list()
    groups = [i["group_id"] for i in groups]
    try:
        msg = event.plain_text.strip()
    except:
        msg = ""
    for gp in groups:
        await bot.send_group_msg(
            group_id=gp, message=text + ((reason + msg) if msg != "" else "")
        )


ed = on_command("ed", permission=SUPERUSER, priority=1)


@ed.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    text = """！！！Bot维护结束！！！
"""

    reason = """
维护结果：

"""
    await bot.send_group_msg(group_id=1037557679, message="Halo")
    groups = await bot.get_group_list()
    groups = [i["group_id"] for i in groups]
    try:
        msg = event.plain_text.strip()
    except:
        msg = ""
    for gp in groups:
        await bot.send_group_msg(
            group_id=gp, message=text + ((reason + msg) if msg != "" else "")
        )
    cmd = "login"
    event.plain_text = cmd
    event.raw_event["raw_message"] = cmd
    event.message = Message(cmd)
    asyncio.create_task(handle_event(bot, event))
