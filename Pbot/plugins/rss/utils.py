import asyncio
from .models import *
import sys

import cq
import feedparser as fp
from nonebot.exception import ActionFailed, ApiNotAvailable, NetworkError, RequestDenied
from nonebot.log import logger

from utils import doc, hourse

from .parsers import *


async def handlerss(
    bot,
    source,
    getfun,
    is_broadcast: bool = True,
    is_fullText: bool = False,
    broadcastgroup: list = [],
):
    loop = asyncio.get_event_loop()
    value = await Rss.query.where(Rss.id == source).gino.first()
    if value == None:
        value = await Rss.create(id=source, dt="-1")
    kwargs = {}
    if "pixiv" in source:
        kwargs["mode"] = source[len("pixiv_") :]
    try:
        ress = await getfun(**kwargs)
    except Exception:
        await bot.send_private_msg(
            user_id=545870222, message=f"rss「{doc[source]}」更新出现异常"
        )
        logger.error(f"rss「{source}」更新出现异常", exc_info=True)
        return

    res, dt, lk, _ = ress[0]
    if dt == "Grab Rss Error!":
        await bot.send_private_msg(
            user_id=545870222, message=f"rss「[{doc[source]}]」更新出现异常"
        )
        logger.error(f"rss「{source}」更新出现异常", exc_info=True)
        return
    if dt != value.dt:
        preview = f"{doc[source]} - {source}:"
        mx = 5
        for item in ress:
            if item[1] != value.dt:
                mx -= 1
                preview += "\n"
                preview += item[-1]
                preview += "\n▲" + item[2]
                if mx == 0:
                    break
            else:
                break
        try:
            await value.update(pre=value.dt, dt=dt).apply()
        except Exception as e:
            pass
        if is_broadcast:
            for gp_id in broadcastgroup:
                try:
                    if gp_id != 145029700 and source == "stz" and is_fullText:
                        continue
                    if source == "stz":
                        for item in res:
                            await bot.send_group_msg(group_id=gp_id, message=item)
                    else:
                        await bot.send_group_msg(
                            group_id=gp_id,
                            message=res[0]
                            if is_fullText
                            else preview + f"\n\n回复 rss {source} 获取详细信息",
                        )
                except (
                    RequestDenied,
                    ApiNotAvailable,
                    NetworkError,
                    ActionFailed,
                ) as e:
                    pass

    Suber = await Sub.query.where(Sub.rss == source).gino.all()
    for item in Suber:
        if item.dt != dt:
            asyncio.run_coroutine_threadsafe(
                sendrss(item["qid"], bot, source, ress), loop,
            )


locks = {}
# num 第一个表示最获取的消息数，第二个表示在此基础上查看的消息数
# -1表示最大，-2表示到已读为止。
async def sendrss(
    qid: int,
    bot,
    source: str,
    ress=None,
    getfun=None,
    num=(-2, 3),
    route=None,
    feedBack=False,
):
    isP = "pixiv" in source
    if qid not in locks:
        locks[qid] = asyncio.Lock()
    async with locks[qid]:
        values = await Sub.query.where(
            (Sub.qid == qid) & (Sub.rss == source)
        ).gino.all()
        if len(values) == 0:
            values = await Rss.query.where(Rss.id == source).gino.all()
            qdt = values[0].pre
        else:
            qdt = values[0].dt
        cnt = 0
        is_read = False
        if ress == None:
            kwargs = {}
            if "pixiv" in source:
                kwargs["mode"] = source[len("pixiv_") :]
            else:
                kwargs["max_num"] = num[0] if num[0] != -2 else -1
            if route != None:
                ress = await getfun(route, (num[0] if num[0] != -2 else -1))
            else:
                ress = await getfun(**kwargs)
        if num[0] == -2:
            for i in range(len(ress)):
                if ress[i][1] == qdt:
                    if i == 0:
                        try:
                            ress = ress[:1]
                        except:
                            ress = ress
                        break
                    ress = ress[:i]
                    break
        if num[1] != -1:
            ress = ress[: min(len(ress), num[1])]

        success_dt = ""
        fail = 0
        for res, dt, link, _ in reversed(ress):
            if is_read == False and dt == qdt:
                is_read = True
            if num[1] != -1 and cnt >= num[1]:
                break
            see = ""
            is_r = is_read
            cnt += 1
            if isP:
                await asyncio.sleep(1)
            await bot.send_private_msg(user_id=qid, message="=" * 19)
            for text in res:
                see = text
                try:
                    await bot.send_private_msg(
                        user_id=qid, message=("已读：\n" if is_r else "") + text
                    )
                    if "[CQ:image" in text and not isP:
                        await asyncio.sleep(1)
                    is_r = False
                    success_dt = dt
                except (
                    RequestDenied,
                    ApiNotAvailable,
                    NetworkError,
                    ActionFailed,
                ) as e:
                    fail += 1
                    logger.error(f"Not ok here. Not ok message 「{see}」")
                    logger.error(f"Processing QQ 「{qid}」, Rss 「{source}」")
                    logger.error("Informing Pzzzzz!")
                    try:
                        await bot.send_private_msg(
                            user_id=545870222,
                            message=f"Processing QQ 「{qid}」, Rss 「{source}」 error! {e}",
                        )
                    except:
                        logger.error("Inform Pzzzzz failed. ")
                    logger.error("Informing the user!")
                    try:
                        await bot.send_private_msg(
                            user_id=qid,
                            message=f"该资讯发送不完整！丢失信息为：「{see}」，请联系管理员。"
                            + ("\n该消息来源：" + link if link != "" else "该资讯link未提供"),
                            auto_escape=True,
                        )
                    except:
                        try:
                            await bot.send_private_msg(
                                user_id=qid,
                                message=f"该资讯发送不完整！丢失信息无法发送，请联系管理员。这可能是由于消息过长导致的"
                                + ("\n该消息来源：" + link if link != "" else "该资讯link未提供"),
                                auto_escape=True,
                            )
                        except:
                            logger.error("Informing failed!")
                    success_dt = dt

        try:
            await bot.send_private_msg(user_id=qid, message="=" * 19)
        except (RequestDenied, ApiNotAvailable, NetworkError, ActionFailed):
            pass
        try:
            await bot.send_private_msg(
                user_id=qid,
                message=f"已发送 {cnt} 条「{doc[source] if source !='自定义路由' else route}」的资讯！{f'其中失败 {fail} 条！' if fail !=0 else ''}咕噜灵波～(∠・ω< )⌒★",
            )
        except (RequestDenied, ApiNotAvailable, NetworkError, ActionFailed):
            logger.error(f"Send Ending Error! Processing QQ 「{qid}」")
        if success_dt != "" and source != "自定义路由" and values[0].dt:
            values[0].dt = success_dt
            await values.apply()
    if feedBack:
        await bot.send_group_msg(
            group_id=feedBack, message=cq.at(qid) + f"「{doc[source]}」的资讯已私信，请查收。"
        )


async def getrss(route: str, max_num: int = -1):
    if route[0] == "/":
        route = route[1:]
    thing = fp.parse(r"http://172.18.0.1:1200/" + route)

    ress = [
        (
            ["暂时没有资讯哦，可能是路由不存在！"],
            thing["entries"][0]["title"] if len(thing["entries"]) > 0 else "something",
            "",
        )
    ]

    cnt = 0

    for item in thing["entries"]:

        if max_num != -1 and cnt >= max_num:
            break

        text = item.title + ("\n" + hourse(item["link"]) if "link" in item else "f")

        text = [text]

        ress.append((text, item["published"] if "published" in item else item.title))

        cnt += 1

    if len(ress) > 1:
        ress = ress[1:]

    return ress


def gtfun(name: str):
    if "pixiv" in name:
        name = "pixiv"
    return getattr(sys.modules[__name__], name)
