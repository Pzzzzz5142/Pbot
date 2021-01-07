#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from Pbot.db import init_db
from Pbot.pixiv import pixiv_login
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

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
driver.register_adapter("cqhttp", CQHTTPBot)
driver.on_startup(init_db)
pixiv_login()

nonebot.load_plugin("nonebot_plugin_apscheduler")
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
