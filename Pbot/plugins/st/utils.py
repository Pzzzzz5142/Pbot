from nonebot.adapters.cqhttp import Bot
import random, base64
from Pbot.utils import *
import Pbot.cq as cq

pixivicurl = "https://api.pixivic.com/"

sauceUrl = r"https://saucenao.com/search.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Authorization": "",
    "Referer": "https://pixivic.com/",
}


async def searchPic(bot: Bot, key_word: str, maxSanityLevel: int = 4):
    datas = {
        "keyword": key_word,
        "pageSize": 15,
        "page": 1,
        "searchType": "original",
        "illustType": "illust",
        "maxSanityLevel": maxSanityLevel,
    }
    async with bot.config.session.get(
        pixivicurl + "illustrations", params=datas, headers=headers
    ) as resp:
        if resp.status != 200:
            return (
                f"网络 {resp.status} 错误哦，咕噜灵波～(∠・ω< )⌒★\n\n如果是401错误，请回复 login 来帮忙识别一下验证🐎哦",
                0,
            )
        ShitJson = await resp.json()
    _id = None
    res = f"暂时没有 {key_word} 的结果哦～"
    Good = [ind for ind in range(0, len(ShitJson["data"]))]
    try:
        while len(Good) != 0:
            pic = random.choice(ShitJson["data"])
            res = await getImage(
                bot.config.session,
                imageProxy(pic["imageUrls"][0]["large"], "img.cheerfun.dev"),
                headers=headers,
            )
            if "失败" in res:
                if "404" in res:
                    ShitJson["data"].remove(pic)
                    continue
                else:
                    res = cq.image(imageProxy_cat(pic["imageUrls"][0]["large"]))
            _id = pic["id"]
            break
    except:
        pass
    if _id == None:
        res = f"暂时没有 {key_word} 的结果哦～"
    return (
        res,
        _id if _id != None else res,
    )


async def auth(bot: Bot, state: dict, **kwargs):
    async with bot.config.session.post(pixivicurl + "users/token", **kwargs) as resp:
        if resp.status != 200:
            if resp.status == 500:
                return "帐号或密码错误！"
            return "验证🐎错误！"
        headers["Authorization"] = resp.headers["Authorization"]
        imgdata = base64.b64decode(state["imageBase64"])
        file = open("/root/image/{}.jpg".format(state["img"].lower()), "wb")
        file.write(imgdata)
        file.close()
        return "ok"


async def sauce(bot: Bot, purl: str) -> str:
    parm = {"db": "999", "output_type": "2", "numres": "3", "url": None}
    parm["url"] = purl

    async with bot.config.session.get(sauceUrl, params=parm, headers=headers) as resp:
        if resp.status != 200:
            return "错误：" + str(resp.status)
        ShitJson = await resp.json()

    if len(ShitJson["results"]) == 0:
        return "啥也没搜到"

    try:
        murl = hourse(ShitJson["results"][0]["data"]["ext_urls"][0])
    except:
        murl = ""

    return (
        cq.image(ShitJson["results"][0]["header"]["thumbnail"])
        + (
            f"\n标题：{ShitJson['results'][0]['data']['title']}"
            if "title" in ShitJson["results"][0]["data"]
            else ""
        )
        + (
            f"\nsource：{ShitJson['results'][0]['data']['source']}"
            if "source" in ShitJson["results"][0]["data"]
            else ""
        )
        + (
            f"\n日文名：{ShitJson['results'][0]['data']['jp_name']}"
            if "jp_name" in ShitJson["results"][0]["data"]
            else ""
        )
        + (
            f"\npixiv id: {ShitJson['results'][0]['data']['pixiv_id']}\n画师: {ShitJson['results'][0]['data']['member_name']}\n画师id: {ShitJson['results'][0]['data']['member_id']}"
            if "pixiv_id" in ShitJson["results"][0]["data"]
            else ""
        )
        + (f"\n来源（请复制到浏览器中打开，不要直接打开）：\n{murl}" if murl != "" else "")
        + "\n相似度："
        + str(ShitJson["results"][0]["header"]["similarity"])
        + "%"
    )
