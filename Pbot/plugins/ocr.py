from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

ocr = on_command("ocr", priority=1)


@ocr.got("img", prompt="发送你要识别的图吧")
async def get_arg(bot: Bot, event: Event, state: dict):
    msg = event.current_arg_images
    if len(msg) > 0:
        state["img"] = event.id
    else:
        await ocr.finish("没有找到图哦。。。。")


@ocr.handle()
async def reco(bot: Bot, event: Event, state: dict):
    data = await bot.call_api(".ocr_image", image=str(state["img"]))
    await ocr.send(data["texts"][0]["text"])

