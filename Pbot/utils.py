import asyncio
import os
from random import randint
from aiohttp import ClientSession
import re, random, datetime

from nonebot.adapters.cqhttp import Bot
import Pbot.cq as cq
from nonebot.log import logger

import nonebot
import os.path as path
import json

doc = {
    "mrfz": "明日方舟",
    "bcr": "公主连接 B服",
    "loli": "忧郁的loli",
    "pprice": "每日生猪价格",
    "bh3": "崩坏3",
    "hpoi": "Hpoi 手办wiki",
    "xl": "b站总运营 乐爷Official",
    "pixiv_day": "Pixiv 每日热榜",
    "pixiv_week": "Pixiv 每周热榜",
    "pixiv_month": "Pixiv 每月热榜",
    "pixiv_week_rookie": "Pixiv 每周新人榜",
    "pixiv_week_original": "Pixiv 每周原创榜",
    "pixiv_day_male": "Pixiv 每日热榜 男性向",
    "pixiv_day_female": "Pixiv 每日热榜 女性向",
    "pixiv_day_r18": "Pixiv 每日热榜 R-18",
    "pixiv_week_r18": "Pixiv 每周热榜 R-18",
    "pixiv_day_male_r18": "Pixiv 每日热榜 男性向 R-18",
    "pixiv_day_female_r18": "Pixiv 每日热榜 女性向 R-18",
    "pixiv_week_r18g": "Pixiv 每周热榜 R18g",
    "stz": "涩图bot",
}


def imageProxy(url: str, prox: str = "pximg.pixiv-viewer.workers.dev") -> str:
    result = url.replace("i.pximg.net", prox)

    result = result.replace("_10_webp", "_70")
    result = result.replace("_webp", "")

    return result


def imageProxy_cat(url):
    return url.replace("i.pximg.net", "i.pixiv.cat")


async def getImage(session: ClientSession, url: str, dir: str = "", **kwargs):
    fd = re.search(r"\?", url)
    if len(dir) > 0 and dir[-1] != "/":
        dir += "/"
    if fd != None:
        url = url[: fd.span()[0]]
    _, pic = path.split(url)
    pic = dir + pic
    if path.exists(nonebot.get_driver().config.imgpath + pic):
        logger.info("发送缓存图片{}".format(pic))
        return cq.image(pic)
    async with session.get(url, **kwargs) as resp:
        if resp.status != 200:
            logger.error("下载图片失败，网络错误 {}。".format(resp.status))
            return "下载图片失败，网络错误 {}。".format(resp.status)

        img = await resp.read()
        with open(nonebot.get_driver().config.imgpath + pic, "wb") as fl:
            fl.write(img)
        logger.info("已保存图片{}".format(pic))
        return cq.image(pic)


def hourse(url: str) -> str:
    a = url
    random.seed(datetime.datetime.now())
    try:
        url = list(url)
        for i in range(5):
            url.insert(random.randint(0, len(url)), "🐎")
        url = "".join(url)
    except:
        url = "（打🐎失败，请复制到浏览器中打开，不要直接打开！）" + a

    return url


def transtime(tm: str, fmt: str = "%a, %d %b %Y %H:%M:%S %Z"):
    try:
        tm = datetime.datetime.strptime(tm, fmt)
    except ValueError:
        pass
    return tm


def get_bot():
    if nonebot.get_bots():
        return list(nonebot.get_bots().values())[0]


async def getSetuLow(sess, r18: bool) -> str:
    random.seed(datetime.datetime.now())
    async with sess.get(
        "https://cdn.jsdelivr.net/gh/ipchi9012/setu_pics@latest/setu{}_index.js".format(
            "_r18" if r18 else ""
        )
    ) as resp:
        if resp.status != 200:
            return "网络错误：" + str(resp.status)
        ShitText = await resp.text()
        ind1, ind2 = ShitText.index("("), ShitText.index(")")
        ShitText = ShitText[ind1 + 1 : ind2]
        ShitList = json.loads(ShitText)
        ch = random.choice(ShitList)

    async with sess.get(
        "https://cdn.jsdelivr.net/gh/ipchi9012/setu_pics@latest/{}.js".format(ch)
    ) as resp:
        if resp.status != 200:
            return "网络错误：" + str(resp.status)
        ShitText = await resp.text()
        ind1 = ShitText.index("(")
        ShitText = ShitText[ind1 + 1 : -1]
        ShitList = json.loads(ShitText)
        ch = random.choice(ShitList)
        return cq.image(
            "https://cdn.jsdelivr.net/gh/ipchi9012/setu_pics@latest/" + ch["path"]
        )


overCall = {}


async def getSetuHigh(
    bot: Bot, r18: bool, keyword: str = "", is_save: bool = True
) -> str:
    random.seed(datetime.datetime.now())
    LoliUrl = r"https://api.lolicon.app/setu/"
    parm = {"apikey": None, "r18": "1", "size1200": "true", "num": 10}
    if keyword != "":
        parm["keyword"] = keyword
    if r18:
        parm["r18"] = 1
    else:
        parm["r18"] = 0
    OverCalled = True
    RequestApi = None
    if bot.config.loliapi:
        RequestApi = bot.config.loliapi
        OverCalled = False
        logger.debug("检测到 Lolicon API ！")
        if bot.config.loliapi in overCall:
            logger.debug(
                f"时间差 {(datetime.datetime.now()-overCall[RequestApi][1]).seconds} 秒。ttl {overCall[RequestApi][1]}"
            )
            if (datetime.datetime.now() - overCall[RequestApi][1]).seconds <= overCall[
                RequestApi
            ][0]:
                logger.debug("主动截断！")
                OverCalled = True

    if bot.config.loliapis and OverCalled:
        logger.debug("检测到多个 Lolicon API ！")
        for api in bot.config.loliapis:
            RequestApi = api
            OverCalled = False
            if api in overCall:
                logger.debug(
                    f"时间差 {(datetime.datetime.now()-overCall[api][1]).seconds} 秒。ttl {overCall[api][1]}"
                )
                if (datetime.datetime.now() - overCall[api][1]).seconds <= overCall[
                    api
                ][0]:
                    logger.debug("主动截断！")
                    OverCalled = True
                else:
                    break

    if OverCalled:
        return await handleOverCall(bot, RequestApi, r18)
    if RequestApi:
        parm["apikey"] = RequestApi
    else:
        logger.warning("未检测到 LoliconAPI 的配置！涩图请求可能受限！")
        parm["num"] = 1
    now = datetime.datetime.now()
    async with bot.config.session.get(LoliUrl, params=parm) as resp:
        if resp.status != 200:
            return None, "网络错误：" + str(resp.status)
        ShitJson = await resp.json()
        if ShitJson["quota"] == 0:
            return await handleOverCall(bot, bot.config.loliapi, r18, ShitJson, now)
        if is_save:
            pic = await getImage(
                bot.config.session,
                ShitJson["data"][0]["url"],
                f"pixiv{'/r18' if r18 else '/'}",
            )
        else:
            pic = cq.image(ShitJson["data"][0]["url"])

        loop = asyncio.get_event_loop()
        for item in ShitJson["data"]:
            asyncio.run_coroutine_threadsafe(
                getImage(
                    bot.config.session, item["url"], f"pixiv{'/r18' if r18 else '/'}",
                ),
                loop,
            )

        return pic, ShitJson["data"][0]


async def handleOverCall(bot: Bot, api, r18, ShitJson: dict = None, now=None):
    if ShitJson:
        overCall[api] = (ShitJson["quota_min_ttl"], now)
    cache = [
        "pixiv/" + ("r18/" if r18 else "") + pic.name
        for pic in os.scandir(bot.config.imgpath + "pixiv/" + ("r18" if r18 else ""))
        if pic.is_file()
    ]
    pic = random.choice(cache)
    fd = re.search("/\d+", pic)
    _id = pic[fd.start() + 1 : fd.end()]
    text = f"现在是缓存时间哦！\n距离下一次在线请求还剩 {overCall[api][0]-(datetime.datetime.now()-overCall[api][1]).seconds+1} 秒。"
    logger.info(re.sub("\n", "", text))
    try:
        text = await getPixivDetail(bot.config.session, _id)
    except:
        pass
    return cq.image(pic), text


async def cksafe(gid: int):
    if gid == 145029700:
        return False
    return True


async def getPixivDetail(session: ClientSession, _id):
    api = r"https://api.imjad.cn/pixiv/v2/"
    parm = {"id": _id}
    async with session.get(api, params=parm) as resp:
        if resp.status != 200:
            raise Exception
        ShitJson = await resp.json()
        return transform(ShitJson)


def transform(data):
    if not isinstance(data, dict):
        return data
    if data["illust"]:
        data = data["illust"]
    return {
        "author": data["user"]["account"],
        "pid": data["id"],
        "tags": [i["name"] for i in data["tags"]],
        "title": data["title"],
    }

