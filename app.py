from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

import logging

token = config.get_config("Settings", "bot_token")

bot = Bot(token=token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
