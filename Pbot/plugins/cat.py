from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER
import Pbot.cq as cq

cat = on_command("cat", permission=SUPERUSER, priority=1)


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
    for pic in pics:
        await cat.send(pic)
    if len(pics) > 2:
        await cat.finish("发送完毕！")


async def catPixiv(bot: Bot, _id: int, p=None, **kwargs):
    parm = {"id": _id}
    async with bot.config.session.get(
        "https://api.imjad.cn/pixiv/v2/", params=parm
    ) as resp:
        if resp.status != 200:
            return ["网络错误哦！{}".format(resp.status)]
        ShitJson = await resp.json()
        total = ShitJson["illust"]["page_count"]
        if p != None:
            if p == "*":
                if total > 1:
                    return ["这是一个有多页的pid！"] + [
                        cq.image("https://pixiv.cat/{}-{}.jpg".format(_id, i))
                        for i in range(1, total + 1)
                    ]
                else:
                    return [cq.image("https://pixiv.cat/{}.jpg".format(_id))]
            elif p > 0 and p <= total:
                return [
                    cq.image(
                        "https://pixiv.cat/{}-{}.jpg".format(_id, p)
                        if total > 1
                        else "https://pixiv.cat/{}.jpg".format(_id)
                    )
                ]
            else:
                return ["页数不对哦~~ 这个 id 只有 {} 页".format(total)]
        if total > 1:
            return ["这是一个有多页的pid！", cq.image("https://pixiv.cat/{}-1.jpg".format(_id))]
        else:
            return [cq.image("https://pixiv.cat/{}.jpg".format(_id))]
