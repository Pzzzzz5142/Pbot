import re
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event


def ckimg(file: str) -> Rule:
    async def _ckimg(bot: Bot, event: Event, state: dict) -> bool:
        for seg in event.message:
            if seg.type == "image" and seg.data["file"] == file:
                return True
        return False

    return Rule(_ckimg)
