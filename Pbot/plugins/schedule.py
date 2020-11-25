from nonebot.sched import scheduler
from Pbot.db import Mg
from nonebot.exception import ActionFailed, ApiNotAvailable, NetworkError, RequestDenied
from Pbot.db import Backup
from Pbot.utils import get_bot


@scheduler.scheduled_job("cron", hour="5", minute="0")
async def _():
    bot = get_bot()
    values = await Mg.query.where(Mg.morningcall == True).gino.all()
    for item in values:
        item = item.gid
        try:
            await bot.send_group_msg(
                group_id=int(item), message=f"Ciallo～(∠・ω< )⌒★，早上好。"
            )
        except (ActionFailed, ApiNotAvailable, NetworkError, RequestDenied):
            pass


@scheduler.scheduled_job("cron", hour="0,6,12,18", minute="0")
async def backup():
    bot = get_bot()
    ls = await bot.get_group_member_list(group_id=bot.config.group, self_id=3418961367)
    await bot.send("ok for ls")
    await Backup.delete.gino.all()
    await bot.send("ok for del")
    for item in ls:
        await Backup.create(qid=item["user_id"], card=item["card"], role=item["role"])
    await bot.send("ok for backup")

