from aiogram import types
from aiogram.dispatcher import FSMContext

from random import randint

from Data import data_base
from Markups.Reply import reply_menu
from States import states_class
from app import dp, bot
import config

from io import BytesIO
from claptcha import Claptcha

import traceback as tr


def create_captcha(capt_num):
    captcha_image = Claptcha(str(capt_num), "FreeMonospaced.ttf", size=(300, 200))
    buf = BytesIO()
    captcha_image.image[1].save(buf, format='JPEG')
    captcha_image_bytes = buf.getvalue()
    return captcha_image_bytes


@dp.message_handler(commands=['start'])
async def command_start(m: types.Message, state: FSMContext):
    try:
        if data_base.get_user(m.from_user.id) is None:
            if m.from_user.username is None:
                await bot.send_message(m.from_user.id,
                                       "Перед началом пользования создайте ссылку на ваш телеграм аккаунт")
            else:
                num = randint(1000, 10000)
                await bot.send_photo(m.from_user.id, create_captcha(str(num)), "Введите капчу")
                await state.update_data(bot_capt=num)
                await states_class.CaptchaState.captcha_num.set()
        else:
            await bot.send_message(m.from_user.id, "Бронирование книг происходит в чате, сделите за постами!")
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'command_start\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(commands=['admin'])
async def command_admin(m: types.Message):
    if data_base.get_user(m.from_user.id) is not None:
        if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
            await bot.send_message(m.from_user.id, "Здравствуйте", reply_markup=reply_menu.admin_menu())


@dp.message_handler(commands=['me'])
async def command_me(m: types.Message):
    try:
        if data_base.get_user(m.from_user.id) is not None:
            books = data_base.get_books()
            text_pre = ''
            text_past = ''
            for book in books:
                for order in data_base.get_book_order(book[1], book[2]):
                    if m.from_user.id == int(order[1]):
                        text_pre += f"{book[1]}\n"
                for order in data_base.get_book_order_past(book[1], book[2]):
                    if m.from_user.id == int(order[1]):
                        text_past += f"{book[1]}\n"
            if len(text_pre) == 0 and len(text_past) == 0:
                await bot.send_message(m.from_user.id,
                                       "Вы еще не брали и не бронировали книги")
            elif len(text_pre) != 0 and len(text_past) == 0:
                await bot.send_message(m.from_user.id,
                                       "Взятые книги\n"
                                       f"{text_pre}")
            elif len(text_pre) == 0 and len(text_past) != 0:
                await bot.send_message(m.from_user.id,
                                       "Забронированные книги\n"
                                       f"{text_past}")
            else:
                await bot.send_message(m.from_user.id,
                                       "Взятые книги\n"
                                       f"{text_pre}\n"
                                       "Забронированные книги\n"
                                       f"{text_past}")
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'command_me\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(commands=['card'])
async def command_card(m: types.Message):
    await bot.send_message(m.from_user.id,
                           "Оплата на любую из карт:\n\n"
                           "💰 Тинькофф: `2200 7008 1112 9443`\n"
                           "💰 Сбербанк: `2202 2015 6344 9137`\n"
                           "(Получатель: Валерия Анатольевна Л)\n\n"
                           "Через СБП: `79199927561`", parse_mode="Markdown")
