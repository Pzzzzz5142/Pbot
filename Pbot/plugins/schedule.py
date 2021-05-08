import nonebot
from Pbot.db import Mg
from nonebot.exception import ActionFailed, ApiNotAvailable, NetworkError, RequestDenied
from Pbot.db import Backup
from Pbot.utils import get_bot, run_sync_fun
from nonebot import require
from Pbot.pixiv import pixiv_login
import Pbot.cq as cq

scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", hour="5", minute="0")
async def _():
    bots = nonebot.get_bots().values()
    values = await Mg.query.where(Mg.morningcall == True).gino.all()
    for item in values:
        for bot in bots:
            item = item.gid
            try:
                await bot.send_group_msg(
                    group_id=int(item), message=f"Ciallo～(∠・ω< )⌒★，早上好。"
                )
                break
            except:
                pass


@scheduler.scheduled_job("cron", hour="0,6,12,18", minute="0")
async def backup():
    bots = nonebot.get_bots().values()
    for bot in bots:
        ls = await bot.get_group_member_list(
            group_id=bot.config.group, self_id=3418961367
        )
        await Backup.delete.gino.all()
        for item in ls:
            await Backup.create(
                qid=item["user_id"], card=item["card"], role=item["role"]
            )
