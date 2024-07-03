# -*- coding: utf-8 -*-
import asyncio
import logging
import time

from aiogram import Bot
from aiogram import Dispatcher

import markup as markup
import texts as texts
import config as config
import app.base as base
base.init()


from app.handlers import buttons, commands
from app.handlers.fsm_handlers import giveDiscount, giveSell, select_user, sellPod, toMarketPlace

dp = Dispatcher()
bot = Bot(token = config.token)

'''
CREATE TABLE marketplace (
    id       INTEGER      PRIMARY KEY AUTOINCREMENT,
    uid      INTEGER (50),
    name     TEXT (50),
    status   TEXT,
    price    INTEGER,
    photo_id INTEGER,
    comment  TEXT (512) 
);
'''

async def main():
    logging.basicConfig(level=logging.INFO)
    time.sleep(5)

    dp.include_router(commands.router)
    dp.include_router(buttons.router)

    dp.include_router(giveDiscount.router)
    dp.include_router(giveSell.router)
    dp.include_router(select_user.router)
    dp.include_router(sellPod.router)
    dp.include_router(toMarketPlace.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    asyncio.run(main())
    