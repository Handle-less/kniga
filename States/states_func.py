from aiogram.types import Message, ParseMode
from aiogram.dispatcher import FSMContext

import random, datetime

from States import states_class
from Data import data_base
from Handlers import commands, admin
from Markups.Inline import inline_product_menu
from Markups.Reply import reply_menu
from app import dp, bot

import os
from io import BytesIO
from claptcha import Claptcha

import traceback as tr


def create_captcha(capt_num):
    captcha_image = Claptcha(str(capt_num), "FreeMonospaced.ttf", size=(300, 200))
    buf = BytesIO()
    captcha_image.image[1].save(buf, format='JPEG')
    captcha_image_bytes = buf.getvalue()
    return captcha_image_bytes


async def elif_m(m: Message, state: FSMContext):
    if m.text != "/start" \
            and m.text != "/admin" \
            and m.text != "/card" \
            and m.text != "/me" \
            and m.text != "Добавить книгу" \
            and m.text != "Время бронирования" \
            and m.text != "Скачать счет за сегодня" \
            and m.text != "Управление счетами" \
            and m.text != "Отменить⬅" \
            or m.photo:
        return True
    else:
        await state.finish()
        if m.text == "Отменить⬅":
            await m.answer("Отменено",
                           reply_markup=reply_menu.admin_menu())
        elif m.text == "/start":
            await commands.command_start(m, state)
        elif m.text == "/admin":
            await commands.command_admin(m)
        elif m.text == "/me":
            await commands.command_me(m)
        elif m.text == "/card":
            await commands.command_card(m)
        elif m.text == "Добавить книгу":
            await admin.add_book_menu(m)
        elif m.text == "Время бронирования":
            await admin.time_book_menu(m)
        elif m.text == "Скачать счет":
            await admin.down_check_menu(m)
        elif m.text == "Управление счетами":
            await admin.checks_menu(m)


@dp.message_handler(state=states_class.CaptchaState.captcha_num)
async def state_captcha(m: Message, state: FSMContext):
    try:
        data_ = await state.get_data()
        if m.text.isdigit():
            user_capt = int(m.text)
            if data_["bot_capt"] == user_capt:
                await bot.send_message(m.from_user.id,
                                       "Введите свой город, будьте внимательны его нельзя будет поменять")
                await states_class.CaptchaState.next()
            else:
                num = random.randint(1000, 10000)
                await bot.send_photo(m.from_user.id, create_captcha(str(num)), "Введите капчу")
                await state.update_data(bot_capt=num)
        else:
            num = random.randint(1000, 10000)
            await bot.send_photo(m.from_user.id, create_captcha(str(num)), "Введите капчу")
            await state.update_data(bot_capt=num)
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_captcha\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.CaptchaState.city)
async def state_city(m: Message, state: FSMContext):
    try:
        await bot.send_message(m.from_user.id,
                               "Поделитесь номером телефона",
                               reply_markup=reply_menu.share_phone())
        await state.update_data(city=m.text)
        await states_class.CaptchaState.next()
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_city\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.CaptchaState.phone, content_types=['contact'])
async def state_phone(m: Message, state: FSMContext):
    try:
        data = await state.get_data()
        data_base.add_user(m.from_user.id,
                           m.from_user.username,
                           m.from_user.full_name,
                           data['city'],
                           str(m.contact.phone_number))
        await state.finish()
        await m.answer('Регистрация завершена')
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_phone\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.AddBook.name)
async def state_add_book(m: Message, state: FSMContext):
    try:
        if await elif_m(m, state):
            if len(m.text) < 50:
                await state.update_data(name=m.text)
                await m.answer("Введите её цену")
                await states_class.AddBook.next()
            else:
                await state.finish()
                await m.answer("Максимальная длина наименования - 50 символов",
                               reply_markup=reply_menu.cancel_state())
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_add_book\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.AddBook.price)
async def state_add_price(m: Message, state: FSMContext):
    try:
        if await elif_m(m, state):
            pric = m.text
            if pric.isdigit():
                await state.update_data(price=m.text)
                await m.answer("Введите кол-во")
                await states_class.AddBook.next()
            else:
                await state.finish()
                await m.answer("Введите число")
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_add_price\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.AddBook.count)
async def state_add_count(m: Message, state: FSMContext):
    try:
        if await elif_m(m, state):
            kol = m.text
            if kol.isdigit():
                await state.update_data(count=m.text)
                await m.answer("Отправьте обложку")
                await states_class.AddBook.next()
            else:
                await state.finish()
                await m.answer("Введите число")
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_add_count\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(content_types=["photo", "text"], state=states_class.AddBook.photo)
async def state_add_photo_2(m: Message, state: FSMContext):
    try:
        if m.document:
            await state.finish()
            await m.answer("Отправьте сжатое изображение", reply_markup=reply_menu.admin_menu())
        elif await elif_m(m, state):
            data = await state.get_data()
            await state.finish()
            await m.answer("Проверьте данные",
                           reply_markup=reply_menu.admin_menu())
            await bot.send_photo(m.from_user.id,
                                 photo=m.photo[-1].file_id,
                                 caption=f"*Ваша книга:* `{data['name']}`\.\n"
                                         f"*Цена:* `{data['price']}`\.\n"
                                         f"*Количество:* `{data['count']}`\.\n\n",
                                 parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=inline_product_menu.dist_book())
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_add_photo_2\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.EditBook.count)
async def state_edit_count(m: Message, state: FSMContext):
    try:
        if await elif_m(m, state):
            count = m.text
            if count.isdigit():
                if int(count) >= 0:
                    data = await state.get_data()
                    data_base.set_book(data["book_name"], int(count))
                    await m.answer(f"Количество установлено на {count}",
                                   reply_markup=inline_product_menu.end_choice())
                else:
                    await m.answer("Кол-во не может быть меньше 0",
                                   reply_markup=reply_menu.admin_menu())
            else:
                await m.answer("Введите число",
                               reply_markup=reply_menu.admin_menu())
            await state.finish()
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_edit_count\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.EditBook.time)
async def state_time_count(m: Message, state: FSMContext):
    try:
        if await elif_m(m, state):
            data = m.text.split('.')
            d = data[0]
            h = data[1].split(':')[0]
            min = data[1].split(':')[1]
            dt = datetime.datetime.today()
            dt = dt.replace(day=int(d), hour=int(h), minute=int(min))
            data_base.set_time(dt.timestamp())
            await m.answer(f"Время установлено на {m.text}",
                           reply_markup=reply_menu.admin_menu())
    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_time_count\n{e} in {error.lineno} row:{error.line}')


@dp.message_handler(state=states_class.FindUser.user)
async def state_find_user(m: Message, state: FSMContext):
    try:
        users = data_base.find_user(m.text)
        if await elif_m(m, state):
            if users:
                await state.finish()
                text = ""
                for user in users:
                    text += f"{user[2]} (@{user[1]})\n"
                await m.answer(text="Найдены пользователи\n\n"
                                    f"{text}",
                               reply_markup=reply_menu.admin_menu())
            else:
                await m.answer("пользователи не найдены")

    except Exception as e:
        await state.finish()
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'state_time_count\n{e} in {error.lineno} row:{error.line}')
