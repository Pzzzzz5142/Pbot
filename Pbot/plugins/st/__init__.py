from loguru import logger
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from Pbot.utils import cksafe
from .utils import searchPic, pixivicurl, auth, sauce, ascii2d, getSetuHigh
import Pbot.cq as cq
from nonebot.rule import regex
import re

st = on_command("st", rule=regex("^st(?: |$)"))


@st.handle()
async def _(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    if msg:
        state["keyword"] = msg


@st.got("keyword", prompt="发送你想搜的图吧！")
async def _(bot: Bot, event: Event, state: dict):
    msg = event.current_arg_images
    if len(msg) > 0:
        state["pic"] = msg[0]
        return
    msg = str(event.message).strip()
    if msg:
        state["keyword"] = msg
    else:
        await st.reject("输入为空哦！！")


@st.handle()
async def _(bot: Bot, event: Event, state: dict):
    if "pic" in state:
        pic, res = await sauce(bot, state["pic"])
        try:
            await st.send(unescape(pic + "\n" + res))
        except:
            await st.send("发送失败了。。。尝试不带缩略图的发送！")
            try:
                await st.send(res)
            except:
                await st.send("不带缩略图的也发送失败了。。。尝试使用ascii2d搜索！")
                res = await ascii2d(bot, state["pic"])
                try:
                    await st.send(res)
                except:
                    await st.finish("ascii2d 发送也失败了。。。尝试私聊搜图可能可行！")
                await st.finish()
        fd = re.search("[0-9]+\.[0-9]*%", res)
        per = float(res[fd.start() : fd.end() - 1])
        ther = 70
        if per < ther:
            await st.send("相似度低于 {}% 正在使用 ascii2d 搜索！".format(ther))
            res = await ascii2d(bot, state["pic"])
            await st.finish(res)
    else:
        if event.group_id:
            safe = await cksafe(event.group_id)
        else:
            safe = False
        res, _id = await getSetuHigh(bot, not safe, state["keyword"])
        if res == None:
            res, _id = await searchPic(
                bot,
                state["keyword"],
            )
            if _id == -1:
                await st.finish("暂时没有搜索到关于 {} 的结果哦~~".format(state["keyword"]))
        await st.send(
            (cq.reply(event.id) if event.detail_type != "private" else "") + res
        )


login = on_command("login")


@login.handle()
async def _(bot: Bot, event: Event, state: dict):
    async with bot.config.session.get(pixivicurl + "verificationCode") as resp:
        if resp.status != 200:
            await login.finish("获取验证码失败")
        ShitJson = await resp.json()
        img = ShitJson["data"]["imageBase64"]
        vid = ShitJson["data"]["vid"]
        state["imageBase64"] = img
        state["vid"] = vid


@login.got("img", prompt=cq.image("base64://{imageBase64}"))
async def _(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()
    if msg:
        state["img"] = msg
    q = {"vid": state["vid"], "value": state["img"]}
    parm = {"username": bot.config.username, "password": bot.config.password}

    res = await auth(bot, state, params=q, json=parm)

    await login.send(cq.reply(event.id) + "正确！" if "ok" == res else res)
