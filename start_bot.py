import asyncio

from aiogram import executor, types

from Handlers import dp
from app import bot
from Handlers.calc import check_time


async def on_startup(dp):
    await bot.set_my_commands([types.BotCommand("start", "Запустить бота"),
                               types.BotCommand("me", "Список взятых/забронированных книг"),
                               types.BotCommand("card", "Реквизиты для оплаты"), ])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(check_time(bot))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
