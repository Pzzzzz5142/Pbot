from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, unescape
from nonebot.permission import SUPERUSER

hhsh = on_command("hhsh", priority=1)

url = r"https://lab.magiconch.com/api/nbnhhsh/guess"


@hhsh.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    argv = event.raw_message.split(" ")
    for i in argv:
        res = await query(bot, i)
        for j in res:
            await hhsh.send(j)


async def query(bot: Bot, someShit):
    data = {"text": someShit}

    async with bot.config.session.post(url, json=data) as resp:
        if resp.status != 200:
            return ["错误：" + str(resp.status)]
        ShitJson = await resp.json()

    ans = []
    for RealShit in ShitJson:
        re = ""
        try:
            for i in RealShit["trans"]:
                re += i + "\n"
        except:
            try:
                for i in RealShit["inputting"]:
                    re += i + "\n"
            except:
                pass
        re = re[:-1]
        if re == "":
            ans.append(f"呐呐呐，没有查到 {RealShit['name']} 的相关结果")
        else:
            ans.append(
                f"""呐，{RealShit['name']} 可能是：
{re}"""
            )

    return ans
