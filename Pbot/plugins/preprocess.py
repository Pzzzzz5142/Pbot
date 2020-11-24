from nonebot.message import event_preprocessor
from nonebot.adapters.cqhttp import Bot, Event


@event_preprocessor
async def pre(bot: Bot, event: Event, state: dict):
    if event.type == "message":
        event.current_arg_images = [
            seg.data["url"] for seg in event.message if seg.type == "image"
        ]

