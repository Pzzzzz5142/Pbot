from nonebot.sched import scheduler
from Pbot.db import Mg
from nonebot.exception import ActionFailed, ApiNotAvailable, NetworkError, RequestDenied
import nonebot
from utils import get_bot


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
