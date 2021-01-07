from pixivpy3 import ByPassSniApi
import nonebot

api = ByPassSniApi()


def pixiv_login():
    global api
    api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
    # api.set_additional_headers({'Accept-Language':'en-US'})
    api.set_accept_language("en-us")
    config = nonebot.get_driver().config
    api.login(config.pixivusername, config.pixivpassword)


def pixiv_api(api_action, *args, **kwargs):
    action = getattr(api, api_action, None)
    if action:
        res = action(*args, **kwargs)
        return res
