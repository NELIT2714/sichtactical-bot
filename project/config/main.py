from project.config.bot import bot
from project.config.dispatcher import dp
from project.i18n.loader import LocaleStorage

from project.config.routers import main_router
from project.middleware import DefaultMiddleware


def setup():
    locales = LocaleStorage()
    locales.load()

    dp.message.middleware(DefaultMiddleware(locales))
    dp.callback_query.middleware(DefaultMiddleware(locales))

    dp.include_router(main_router)

    return bot, dp
