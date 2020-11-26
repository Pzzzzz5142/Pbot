from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.permission import SUPERUSER

call = on_command("call", priority=1)


@call.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    await bot.send_group_msg(group_id=1037557679, message="Halo")
