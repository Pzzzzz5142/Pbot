from nonebot import on_command
from nonebot.adapters.cqhttp.utils import unescape
from nonebot.message import handle_event
from nonebot.adapters.cqhttp import Bot, Event, Message
from nonebot.permission import SUPERUSER
import asyncio
from .models import MusicPoll
from glob import glob
from Pbot.db import Quser
import random
from Pbot.cq import record

dp = on_command("poll", priority=1)


def choices(*args) -> str:
    return "\n".join([str(ind) + "、" + item for ind, item in enumerate(args)])


@dp.handle()
async def firsthandle(bot: Bot, event: Event, state: dict):
    if event.detail_type != "private":
        await dp.finish("该功能仅限私聊使用！本次投票已结束！")
    await dp.send("欢迎宁参与我的毕设👏👏👏！")
    val = await Quser.query.where(Quser.qid == int(event.user_id)).gino.first()
    if val != None and (val.level != -1):
        await dp.send("啊，看起来你已经评价过了啊！那让我们直接开始吧！")
        state["first"] = False
    else:
        state["first"] = True
        await asyncio.sleep(2)
        await dp.send("👴的毕设题目是使用人工智能作曲。因此想请你听一听作出的曲好不好听。")
        await asyncio.sleep(2)
        await dp.send("这是一个问卷调查，所以在开始之前先问一下你的音乐水平如何呢？（指对乐理的理解（用阿拉伯数字回复")
        await dp.send(choices("我可太Pro了", "颇有研究", "只能会一点点不能会多了", "完 全 不 懂 ！"))


@dp.handle()
async def secondhandle(bot: Bot, event: Event, state: dict):
    if event.detail_type != "private":
        await dp.finish("该功能仅限私聊使用！本次投票已结束！")
    if state["first"]:
        val = await Quser.query.where(Quser.qid == int(event.user_id)).gino.first()
        msg = str(event.message).strip()
        if msg == "e":
            await dp.finish("Bye")
        try:
            msg = int(msg)
            if msg > 3 or msg < 0:
                raise Exception
        except:
            await dp.reject("请以阿拉伯数字回复！或者回复 'e' 退出")
        if val != None:
            await val.update(level=msg).apply()
        elif val == None:
            await Quser.create(qid=int(event.user_id), level=msg)
        await dp.send("Ok，我已经记录下来了")
    await dp.send("下面宁将听到的这些歌曲是完全由人工智能生成。每次评测给的模型顺序都是随机的。Enjoy")
    await asyncio.sleep(1)

    songs = [
        "/root/remi_cov_mp3/*",
        "/root/base_remi_mp3/*",
        "/root/top5_div2_mp3/*",
        "/root/div2_mp3/*",
        "/root/result_mp3/*",
    ]

    for ind in range(5):
        await dp.send("这是第{}个模型生成的歌曲（共两首）：".format(ind + 1))

        model = random.choice(songs)

        songs.remove(model)

        state[f"{ind+1}"] = model[6:-6]
        model = glob(model)

        for s in range(2):
            retry = 0
            song = random.choice(model)
            success = False
            while retry < 5:
                try:
                    await dp.send(record(song))
                    success = True
                    break
                except:
                    retry += 1
                    continue
            if not success:
                await dp.send(f"第{s+1}首歌曲发送失败了。。。")

        await asyncio.sleep(2)

    await dp.send("你觉得那个模型的歌曲最好呢？")

    state["now"] = 5
    state["used"] = []


@dp.receive()
async def optionhandle(bot: Bot, event: Event, state: dict):
    if event.detail_type != "private":
        await dp.finish("该功能仅限私聊使用！本次投票已结束！")
    msg = str(event.message).strip()
    if msg == "e":
        await dp.pause("Ok，请问你有啥评价想说的吗？")
    try:
        msg = int(msg)
        if msg > 5 or msg < 1 or msg in state["used"]:
            raise Exception
    except:
        await dp.reject("请以阿拉伯数字回复，切勿重复！或者回复 'e' 退出")

    if state["now"] == 5:
        val = await MusicPoll.query.where(MusicPoll.id == int(event.user_id)).gino.all()
        if len(val) > 0:
            val = max([i.ind for i in val])
        else:
            val = 0
        kwargs = {
            "id": int(event.user_id),
            state[str(msg)]: state["now"],
            "ind": val + 1,
        }
        state["db"] = await MusicPoll.create(**kwargs)
    else:
        kwargs = {state[str(msg)]: state["now"]}
        await state["db"].update(**kwargs).apply()

    state["used"].append(msg)

    state["now"] = state["now"] - 1

    if state["now"] > 0:
        await dp.send(f"你觉得那个模型的歌曲第{5-state['now']+1}好听呢？（回复 'e' 进入最后一个问题！！")
        await dp.reject()

    await dp.pause("Ok，请问你有啥评价想说的吗？")


@dp.handle()
async def commenthandle(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()[:100]
    await state["db"].update(comment=msg).apply()
    await dp.finish("Ok，你的投票已经被记录！感谢参与！期待你的下次参与！")