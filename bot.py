#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
import aiohttp
from Pbot.db import init

# Custom your logger
#
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.on_startup(init)

nonebot.load_plugins("Pbot/plugins")

# Modify some config / config depends on loaded configs
#
# config = nonebot.get_driver().config
# do something...

config = nonebot.get_driver().config
if config.imgpath and config.imgpath[-1] != "/":
    config.imgpath += "/"

if __name__ == "__main__":
    nonebot.run(app="bot:app")
