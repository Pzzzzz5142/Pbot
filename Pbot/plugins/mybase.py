from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.permission import SUPERUSER

echo = on_command("echo", priority=1)


@echo.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    print(str(event.message))
    await echo.finish(str(event.raw_message))


say = on_command("say", priority=1, permission=SUPERUSER)


@say.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    await say.finish(unescape(str(event.message)))
