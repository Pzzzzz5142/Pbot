import re
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event

def ckimg() -> Rule:

    async def _ckimg(bot: Bot, event: Event, state: dict) -> bool:
        for seg in event.message:
            if seg.type=='image' and seg.data['file']=='b407f708a2c6a506342098df7cac4a57.image':
                return True
        return False

    return Rule(_ckimg)