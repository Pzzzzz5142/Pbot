from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from argparse import ArgumentParser
from langdetect import detect
import random
import hashlib
import urllib

wm = on_command("wm", priority=1)


@wm.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    arg = event.plain_text.strip()

    parser = ArgumentParser()

    parser.add_argument("--fr", "-f", type=str, default="no")
    parser.add_argument("--to", "-t", type=str, default="no")
    parser.add_argument("token", type=str, default="", nargs="+")
    argv = parser.parse_args(arg.split(" "))

    arg = " ".join(argv.token)

    if arg == "":
        await wm.finish("输入不能为空哦！")

    state["fr"] = detect(arg) if argv.fr == "no" else argv.fr

    if state["fr"][:2] == "zh":
        state["fr"] = "zh"

    if argv.to == "no":
        if state["fr"] == "zh":
            state["to"] = "en"
        else:
            state["to"] = "zh"
    else:
        state["to"] = argv.to

    if argv.fr == "no":
        state["fr"] = "auto"

    state["token"] = arg


@wm.handle()
async def trans(bot: Bot, event: Event, state: dict):
    myurl = "/api/trans/vip/translate"
    q = state["token"]
    fromLang = state["fr"]  # 原文语种
    toLang = state["to"]  # 译文语种
    salt = random.randint(32768, 65536)
    sign = str(bot.config.baiduapi) + q + str(salt) + bot.config.baidukey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = (
        myurl
        + "?appid="
        + str(bot.config.baiduapi)
        + "&q="
        + urllib.parse.quote(q)
        + "&from="
        + fromLang
        + "&to="
        + toLang
        + "&salt="
        + str(salt)
        + "&sign="
        + sign
    )
    async with bot.config.session.get("https://fanyi-api.baidu.com" + myurl) as resp:
        if resp.status != 200:
            pass
        ShitAns = await resp.json()
    try:
        ans = [i["dst"] for i in ShitAns["trans_result"]]
        ans = "\n".join(ans)
    except:
        await wm.finish("翻译错误，原因是：" + ShitAns["error_code"])
        return

    await wm.finish("翻译结果为：\n" + ans)
