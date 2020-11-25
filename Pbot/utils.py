from aiohttp import ClientSession
import re, random, datetime
import Pbot.cq as cq

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


async def getImage(session: ClientSession, url: str, **kwargs):
    fd = re.search(r"\?", url)
    if fd != None:
        url = url[: fd.span()[0]]
    async with session.get(url, **kwargs) as resp:
        if resp.status != 200:
            return "下载图片失败，网络错误 {}。".format(resp.status)
        _, pic = path.split(url)
        img = await resp.read()
        with open(nonebot.get_driver().config.imgpath + pic, "wb") as fl:
            fl.write(img)
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


async def getSetu(sess, r18: bool) -> str:
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
        ind1 = random.randint(0, len(ShitList))

    async with sess.get(
        "https://cdn.jsdelivr.net/gh/ipchi9012/setu_pics@latest/{}.js".format(
            ShitList[ind1]
        )
    ) as resp:
        if resp.status != 200:
            return "网络错误：" + str(resp.status)
        ShitText = await resp.text()
        ind1 = ShitText.index("(")
        ShitText = ShitText[ind1 + 1 : -1]
        ShitList = json.loads(ShitText)
        ind1 = random.randint(0, len(ShitList))
        return cq.image(
            "https://cdn.jsdelivr.net/gh/ipchi9012/setu_pics@latest/"
            + ShitList[ind1]["path"]
        )


async def cksafe(gid: int):
    if gid != 145029700:
        return False
    return True
