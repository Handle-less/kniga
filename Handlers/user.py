from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from Data import data_base
from Markups.Inline import inline_product_menu
import config
from app import dp, bot

from time import time

import traceback as tr


@dp.callback_query_handler(Text(startswith="call_get"))
async def call_get_book(call: CallbackQuery):
    try:
        if data_base.get_user(call.from_user.id) is not None:
            data = call.data.split('_')
            if data[2] == "yes":
                data = call.message.caption.split("\n")
                book_name = data[0]
                if data_base.get_book(book_name) is not None:
                    orders = data_base.get_count_order(book_name)
                    count = int(len(orders))
                    total = data_base.get_book(book_name)[2]
                    data_base.add_order(int(time()), call.from_user.id, book_name, int(data[1].split(':')[1].strip()))
                    await call.message.edit_caption(call.message.caption,
                                                    reply_markup=inline_product_menu.get_no(count + 1, total))
                    if count < total:
                        await bot.send_message(config.get_config("Settings", "chat"),
                                               f"{book_name}\n"
                                               f"Взял(а): {call.from_user.full_name} (@{call.from_user.username})",
                                               reply_to_message_id=call.message.message_id)
                    else:
                        await bot.send_message(config.get_config("Settings", "chat"),
                                               f"{book_name}\n"
                                               f"Забронировал(а): {call.from_user.full_name} (@{call.from_user.username})",
                                               reply_to_message_id=call.message.message_id)
                else:
                    await call.message.edit_caption(call.message.caption)
            elif data[2] == "no":
                data = call.message.caption.split("\n")
                book_name = data[0]
                orders = data_base.get_count_order(book_name)
                count = int(len(orders))
                total = data_base.get_book(book_name)[2]
                if len(data_base.get_order(call.from_user.id, book_name)) != 0:
                    for i in reversed(orders):
                        if int(i[1]) == call.from_user.id:
                            data_base.delete_order(i[0], call.from_user.id)
                            await call.message.edit_caption(call.message.caption,
                                                            reply_markup=inline_product_menu.get_no(count - 1, total))
                            await bot.send_message(config.get_config("Settings", "chat"),
                                                   f"{book_name}\n"
                                                   f"Отказался(ась): {call.from_user.full_name} (@{call.from_user.username})",
                                                   reply_to_message_id=call.message.message_id)
                            break
                else:
                    await call.answer("Вы не брали книгу")

        else:
            await call.answer("Зарегистрируйтесь в боте")
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'call_get_book\n{e} in {error.lineno} row:{error.line}')
