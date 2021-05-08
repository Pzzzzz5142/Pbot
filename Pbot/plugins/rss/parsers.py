import asyncio
import re
from datetime import datetime, timedelta

import Pbot.cq as cq
import feedparser as fp
import nonebot
import pytz
from bs4 import BeautifulSoup, Comment
from operator import itemgetter

from Pbot.utils import getImage, imageProxy, transtime


async def rssBili(uid, max_num: int = -1):
    thing = fp.parse(r"http://172.18.0.1:1200/bilibili/user/dynamic/" + str(uid))

    ress = [
        (
            ["暂时没有有用的新资讯哦！"],
            (
                thing["entries"][0]["title"]
                if len(thing["entries"]) > 0
                else "Grab Rss Error!"
            ),
            "",
        )
    ]

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break

        if (
            ("封禁公告" in item.summary)
            or ("小讲堂" in item.summary)
            or ("中奖" in item.summary)
            or ("转发" in item.summary)
        ):
            continue

        fdres = re.match(r".*?<br />", item.summary, re.S)

        if fdres == None:
            text = item.summary
        else:
            text = fdres.string[int(fdres.span()[0]) : fdres.span()[1] - len("<br />")]

        text = re.sub("<img alt.*>", "", text)

        while len(text) > 1 and text[-1] == "\n":
            text = text[:-1]

        pics = re.findall(
            r"https://(?:(?!https://).)*?\.(?:jpg|jpeg|png|gif|bmp|tiff|ai|cdr|eps)\"",
            item.summary,
            re.S,
        )
        text = [text]

        sess = nonebot.get_driver().config.session
        for i in pics:
            i = i[:-1]
            pic = await getImage(sess, i)
            if pic != None:
                text.append(pic)
        ress.append(
            (
                text,
                item["published"],
                item["link"] if "link" in item and item["link"] != "" else "",
                item["title"],
            )
        )

        cnt += 1

    if len(ress) > 1:
        ress = ress[1:]

    return ress


async def bcr(max_num: int = -1):
    return await rssBili(353840826, max_num)


async def xl(max_num: int = -1):
    return await rssBili(49458759, max_num)


async def bh3(max_num: int = -1):
    def dfs(thing):
        if isinstance(thing, Comment):
            return ""
        if isinstance(thing, str):
            return thing
        if thing.name == "br":
            return "<br/>"
        res = ""
        for item in thing.contents:
            res += dfs(item)
        return res

    thing = fp.parse(r"http://172.18.0.1:1200/mihoyo/bh3/latest")

    ress = [
        (
            ["暂时没有有用的新公告哦！"],
            (
                thing["entries"][0]["title"]
                if len(thing["entries"]) > 0
                else "Grab Rss Error!"
            ),
            "",
            "",
        )
    ]

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break

        sp = BeautifulSoup(item.summary, "lxml")

        pp = sp.find_all("p")

        res = "标题：" + item["title"] + "\n"
        for i in pp:
            ans = dfs(i)
            if ans != "":
                res += "\n" + (ans if ans != "<br/>" else "")

        if "封禁" in res or "封号" in res:
            continue

        ress.append(
            (
                [res],
                item["published"],
                item["link"] if "link" in item and item["link"] != "" else "",
                item["title"],
            )
        )

    if len(ress) > 1:
        ress = ress[1:]

    return ress


async def hpoi(max_num: int = -1):
    def dfs(x) -> str:
        if isinstance(x, str):
            x = x.strip()
            return x if x != "\n" else ""
        res = ""
        for i in x.contents:
            res += dfs(i)
        return res

    thing = fp.parse(r"http://172.18.0.1:1200/hpoi/info/all")

    ress = [
        (
            ["暂时没有有用的新资讯哦！"],
            (
                thing["entries"][0]["title"]
                if len(thing["entries"]) > 0
                else "Grab Rss Error!"
            ),
            "",
            "",
        )
    ]
    t_max_num = max_num
    max_num = -1

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break

        sess = nonebot.get_driver().config.session
        async with sess.get(item["link"]) as resp:
            if resp.status != 200:
                return "Html页面获取失败！错误码：" + str(resp.status)
            ShitHtml = await resp.text()

        sp = BeautifulSoup(ShitHtml, "lxml")

        ShitTime = sp.find_all(class_="left-item-content")
        ShitAttr = sp.find(class_="table table-condensed info-box")

        ShitAttr = ShitAttr.find_all("tr")

        ShitPic = sp.find("a", class_="thumbnail fix-thumbnail-margin-10")["href"]
        ShitPic = await getImage(sess, ShitPic)

        tm = None
        text = ""

        for i in ShitAttr:
            x = dfs(i)
            if x != "" and x[0] != "外":
                text += x + "\n"
        text = [ShitPic, text[:-1]]

        for i in ShitTime:
            content = i.contents[0]
            content = content.strip()
            x = transtime(content, "%a %b %d %H:%M:%S %Z %Y 创建")
            if isinstance(x, str):
                x = transtime(content[:16], "%Y-%m-%d %H:%M")
            if not isinstance(x, str):
                tm = x if tm == None or tm < x else tm

        ress.append(
            (
                text,
                tm,
                item["link"] if "link" in item and item["link"] != "" else "",
                None,
            )
        )

        cnt += 1

    if len(ress) > 1:
        ress = ress[1:]

    ress.sort(key=lambda x: x[1], reverse=True)

    return ress[:t_max_num]


async def loli(max_num: int = -1):
    return None


async def mrfz(max_num: int = -1):
    def dfs(thing):
        if isinstance(thing, str):
            return thing
        if thing.name == "br":
            return "<br/>"
        res = ""
        for item in thing.contents:
            res += dfs(item)
        return res

    thing = fp.parse(r"http://172.18.0.1:1200/arknights/news")

    ress = [
        (
            ["暂时没有有用的新公告哦！"],
            (
                thing["entries"][0]["title"]
                if len(thing["entries"]) > 0
                else "Grab Rss Error!"
            ),
            "",
            "",
        )
    ]

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break

        sp = BeautifulSoup(item.summary, "lxml")

        pp = sp.find_all("p")

        res = "标题：" + item["title"] + "\n"
        for i in pp:
            ans = dfs(i)
            if ans != "":
                res += "\n" + (ans if ans != "<br/>" else "")

        if "封禁" in res:
            continue

        ress.append(
            (
                [res],
                item["published"],
                item["link"] if "link" in item and item["link"] != "" else "",
                item["title"],
            )
        )

    if len(ress) > 1:
        ress = ress[1:]

    return ress


async def pixiv(mode: str = "day"):
    searchapi = r"https://api.imjad.cn/pixiv/v2/"

    now = datetime.now(pytz.timezone("Asia/Shanghai"))

    retry = 3

    now -= timedelta(days=2)

    ress = [([f"在尝试 {retry} 遍之后，还是没有爬到图片呢。。。"], "Grab Rss Error!", "", "")]

    datas = {"mode": mode, "type": "rank", "date": now.strftime("%Y-%m-%d")}

    sess = nonebot.get_driver().config.session
    ShitJson = {}

    while retry != 0:
        async with sess.get(searchapi, params=datas) as resp:
            if resp.status != 200:
                return "网络错误哦，咕噜灵波～(∠・ω< )⌒★"
            ShitJson = await resp.json()
            if "illusts" in ShitJson:
                break
            await asyncio.sleep(1)
        retry -= 1
    if "illusts" not in ShitJson:
        return ress

    res = []
    _id = -1
    for item in ShitJson["illusts"]:
        res.append(cq.image(imageProxy(item["image_urls"]["medium"])))
        _id = item["id"]
    ress.append((res, _id, "", ""))

    if len(ress) > 1:
        ress = ress[1:]

    return ress


async def stz(max_num: int = -1):
    return await rssBili(168687092, max_num)


async def pprice(max_num: int = -1):
    thing = fp.parse(r"http://172.18.0.1:1200/pork-price")

    ress = [
        (
            ["暂时没有猪肉价格哦！"],
            (
                thing["entries"][0]["title"]
                if len(thing["entries"]) > 0
                else "Grab Rss Error!"
            ),
            "",
            "",
        )
    ]

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break
        ress.append(
            (
                [item["title"]],
                item["title"],
                item["link"] if "link" in item and item["link"] != "" else "",
                item["title"],
            )
        )

        cnt += 1

    if len(ress) > 1:
        ress = ress[1:]

    return ress

