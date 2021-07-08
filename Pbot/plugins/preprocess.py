from nonebot.message import event_preprocessor
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.exception import IgnoredException


@event_preprocessor
async def pre(bot: Bot, event: Event, state: dict):
    if event.type == "message":
        event.current_arg_images = [
            seg.data["url"] for seg in event.message if seg.type == "image"
        ]
        if (
            event.self_id == "3418961367"
            and event.detail_type == "group"
            and event.group_id == 145029700
        ):
            raise IgnoredException("该群有两个机器人")


"""
    if event.detail_type != "group":
        return
    async with db.pool.acquire() as conn:
        values = await conn.fetch(
            "select * from mg where gid = {}".format(event.group_id)
        )
        if "on" == event.raw_message[:2] or "off" == event.raw_message[:3]:
            return
        if len(values) == 0:
            raise CanceledException("该群不处于白名单中")
"""
