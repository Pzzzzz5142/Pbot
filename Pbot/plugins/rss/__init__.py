from nonebot import on_command
from nonebot.message import handle_event
from nonebot.adapters.cqhttp import Bot, Event, unescape, Message
from argparse import ArgumentParser
from Pbot.db import Mg
from Pbot.utils import doc, get_bot
from .utils import sendrss, getrss, gtfun, handlerss
import Pbot.cq as cq
from .models import *
import asyncio
from nonebot import require
import nonebot

scheduler = require("nonebot_plugin_apscheduler").scheduler

rss = on_command("rss")
gift = on_command("带礼包")
NOUPDATE = ["loli", "hpoi"]
NOBROADCAST = ["gcores"]
FULLTEXT = ["pprice", "stz", "boss_notice"]


@scheduler.scheduled_job("interval", minutes=20)
async def _():
    bots = nonebot.get_bots().values()

    loop = asyncio.get_event_loop()
    values = await Mg.query.where(Mg.rss == True).gino.all()
    values = [int(item.gid) for item in values]
    for key in doc:
        if key == "boss_notice":
            is_ghz = await Mg.query.where(
                (Mg.ghz == True) & (Mg.gid == 145029700)
            ).gino.first()
            if is_ghz == None:
                continue
        if key in NOUPDATE or "pixiv" in key:
            continue
        for bot in bots:
            asyncio.run_coroutine_threadsafe(
                handlerss(
                    bot,
                    key,
                    gtfun(key),
                    key not in NOBROADCAST,
                    key in FULLTEXT,
                    values,
                ),
                loop,
            )


@rss.handle()
async def args(bot: Bot, event: Event, state: dict):
    parser = ArgumentParser()
    subparser = parser.add_mutually_exclusive_group()
    subparser.add_argument("-s", "--subs", nargs="+", help="订阅指定的 rss 源")
    subparser.add_argument("-r", "--route", nargs="+", help="获取自定路由的 rss 源的资讯")
    subparser.add_argument("-d", "--delete", nargs="+", help="删除 rss 订阅")
    subparser.add_argument(
        "-l", "--list", action="store_true", default=False, help="列出已订阅的源"
    )
    subparser.add_argument("-a", "--add", help="开通rss源")
    parser.add_argument("rss", nargs="*", help="获取已存在的 rss 源资讯")
    argv = parser.parse_args(event.plain_text.strip().split(" "))
    state["ls"] = []
    ls = []
    state["list"] = argv.list
    if argv.list:
        return
    if argv.subs != None:
        state["subs"] = argv.subs
        ls = argv.subs
    if argv.delete != None:
        state["del"] = argv.delete
        ls = argv.delete
    if argv.rss != []:
        state["rss"] = argv.rss
        ls = argv.rss
    if argv.route != None:
        state["route"] = argv.route
        state["ls"] = argv.route
        if len(state["ls"]) == 0:
            await rss.finish("查询路由地址不能为空哦！")
        return
    if argv.add != None:
        await rss.finish("目前不支持哦！！！")
        await rss.send(str(event.user_id))
        # result = await add_rss(argv.add.strip(), str(event.user_id))

    ls = list(set(ls))
    if event.detail_type == "group":
        safe = await Mg.query.where(Mg.gid == event.group_id).gino.all()
        print(len(safe))
        if len(safe) > 0 and safe[0].safe:
            ls = [i for i in ls if "r18" not in i]

    for key in doc:
        if key in ls[:]:
            state["ls"].append((gtfun(key), key))
            ls.remove(key)

    if len(ls) > 0 and " ".join(ls).strip() != "":
        await rss.send(
            unescape(
                "没有添加「{}」的订阅源！请联系".format(" ".join(ls)) + cq.at(545870222) + "添加订阅！"
            )
        )
    if len(state["ls"]) == 0:
        await rss.finish("本次资讯{}为空哦！".format("查看" if state["rss"] != [] else "订阅"))


@rss.handle()
async def firstHandle(bot: Bot, event: Event, state: dict):
    if "subs" in state:
        for _, item in state["ls"]:
            await Sub.create(qid=event.user_id, dt="No Information", rss=item)
            await rss.send(f"「{doc[item]}」的资讯已添加订阅了！有新资讯发布时，会私信你哦！")
            # except asyncpg.exceptions.ForeignKeyViolationError:
            #    await session.send(f"貌似系统并没有支持该订阅源的订阅！")
            #    logger.error("no", exc_info=True)
            # except asyncpg.exceptions.UniqueViolationError:
            #    await session.send(f"你已经添加过「{doc[item]}」的资讯订阅啦！")
            # except:
            #    await session.send(
            #        f"发生未知错误！错误详细信息已记录了在log中！\n定位 message id 为：{event.message_id}"
            #    )
            #    logger.error("some rss issue", exc_info=True)

    elif "route" in state:
        for rt in state["ls"]:
            resp = await sendrss(
                event.user_id,
                bot,
                "自定义路由",
                None,
                getrss,
                (1, 1),
                route=rt,
            )
            if resp and event.detail_type != "private":
                await rss.send(unescape(cq.at(event.user_id) + f"「{rt}」的资讯已私信，请查收。"))

    elif "del" in state:
        fail = []
        success = []
        for _, dl in state["ls"]:
            resp = await Sub.delete.where(
                (Sub.qid == event.user_id) & (Sub.rss == dl)
            ).gino.status()
            print(resp)
            if resp[len("delete ") :] == "0":
                fail.append(doc[dl])
            else:
                success.append(doc[dl])
        if len(fail) > 0:
            await rss.send(
                cq.at(event.user_id)
                + f"这{'个' if len(fail)==1 else '些'}源「{'、'.join(fail)}」不在你的订阅列表里面哦～"
            )
        if len(success) > 0:
            await rss.send(
                cq.at(event.user_id) + f" 取消订阅「{'、'.join(success)}」成功！可喜可贺，可喜可贺！"
            )
    elif state["list"]:
        values = await Sub.query.where(Sub.qid == event.user_id).gino.all()
        if len(values) == 0:
            await rss.finish("貌似你没有订阅任何 rss 源")
        await rss.send(
            cq.at(event.user_id)
            + "以下是你已订阅的源：\n{}".format(
                "\n".join([doc[i.rss] + " - " + i.rss for i in values])
            )
        )

    else:
        loop = asyncio.get_event_loop()
        for item, nm in state["ls"]:
            asyncio.run_coroutine_threadsafe(
                sendrss(
                    event.user_id,
                    bot,
                    nm,
                    None,
                    item,
                    feedBack=event.group_id
                    if event.detail_type != "private"
                    else False,
                ),
                loop,
            )


@gift.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    cmd = "rss pixiv_day_r18 pixiv_week_r18 pixiv_day_male_r18"
    event.raw_message = cmd
    event.raw_event["raw_message"] = cmd
    event.message = Message(cmd)
    asyncio.create_task(handle_event(bot, event))


up = on_command("up", priority=1)


@up.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    loop = asyncio.get_event_loop()
    values = await Mg.query.where(Mg.rss == True).gino.all()
    values = [int(item.gid) for item in values]
    for key in doc:
        if key in NOUPDATE or "pixiv" in key:
            continue
        asyncio.run_coroutine_threadsafe(
            handlerss(
                bot,
                key,
                gtfun(key),
                key not in NOBROADCAST,
                key in FULLTEXT,
                values,
            ),
            loop,
        )
