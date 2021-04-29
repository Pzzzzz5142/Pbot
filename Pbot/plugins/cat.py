from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from Pbot.utils import getPixivDetail, getImage
import Pbot.cq as cq

cat = on_command("cat", priority=1)


@cat.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    p = None
    _id = None
    ls = []
    try:
        ls = str(event.message).strip().split("-")
        _id = ls[0]
        _id = int(_id)
    except:
        await cat.finish("请输入正确格式的pid哦~~")
    try:
        p = ls[1]
        if p != "*":
            p = int(p)
            if p == 0:
                raise Exception
    except IndexError:
        pass
    except:
        await cat.finish("页码不对哦~~页码从0开始。。")
    await cat.send(cq.reply(event.id) + "尝试发送中，。，。，。")
    pics = await catPixiv(bot, _id, p)
    for ind, pic in enumerate(pics):
        if len(pic) > 0 and pic[0] == "h":
            try:
                pic = await getImage(bot.config.session, pic)
            except:
                await cat.send("第 {} 页发送失败了。。但是已经缓存。。尝试重发可能可行！".format(ind))
        await cat.send(pic)
    if len(pics) > 2:
        await cat.finish("发送完毕！")


async def catPixiv(bot: Bot, _id: int, p=None, **kwargs):
    data = {"p": _id}
    async with bot.config.session.post(
        "https://api.pixiv.cat/v1/generate", json=data
    ) as resp:
        if resp.status != 200:
            return ["网络错误：" + str(resp.status)]
        ShitJson = await resp.json()
        if ShitJson["success"]:
            total = len(ShitJson["original_urls"]) if ShitJson["multiple"] else 1
        else:
            return [ShitJson["error"]]
    if p != None:
        if p == "*":
            if total > 1:
                return ["这是一个有 {} 页的pid！".format(total)] + [
                    "https://pixiv.cat/{}-{}.jpg".format(_id, i)
                    for i in range(1, total + 1)
                ]
            else:
                return [cq.image("https://pixiv.cat/{}.jpg".format(_id))]
        elif p > 0 and p <= total:
            return [
                "https://pixiv.cat/{}-{}.jpg".format(_id, p)
                if total > 1
                else "https://pixiv.cat/{}.jpg".format(_id)
            ]
        else:
            return ["页数不对哦~~ 这个 id 只有 {} 页".format(total)]
    if total > 1:
        return ["这是一个有多页的pid！", "https://pixiv.cat/{}-1.jpg".format(_id)]
    else:
        return ["https://pixiv.cat/{}.jpg".format(_id)]
