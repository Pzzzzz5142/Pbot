from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.permission import SUPERUSER

echo = on_command("echo", priority=1)


@echo.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    print(str(event.message))
    await echo.finish(str(event.plain_text))


say = on_command("say", priority=1, permission=SUPERUSER)


@say.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    await say.finish(unescape(str(event.message)))
    pass

get_info=on_command("inin")

@get_info.handle()
async def fh(bot: Bot, event: Event, state: dict):
    json=await bot.call_api("get_stranger_info",user_id=str(event.message))
    await get_info.finish(str(json))