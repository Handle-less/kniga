import math
import time

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode, Message
from aiogram.dispatcher.filters import Text

from Data import data_base, xl
from Markups.Reply import reply_menu
from Markups.Inline import inline_product_menu
from States import states_class
import config
from app import dp, bot

from datetime import datetime

import traceback as tr


@dp.message_handler(text="Добавить книгу")
async def add_book_menu(m: Message):
    if data_base.get_user(m.from_user.id) is not None:
        if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
            await bot.send_message(m.from_user.id, "Введите название книги\n"
                                                   "максимальная длина наименования - 50 символов",
                                   reply_markup=reply_menu.cancel_state())
            await states_class.AddBook.name.set()


@dp.message_handler(text="Время бронирования")
async def time_book_menu(m: Message):
    if data_base.get_user(m.from_user.id) is not None:
        if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
            if data_base.get_time()[0] == 0:
                await bot.send_message(m.from_user.id,
                                       "Добавьте книгу")
            else:
                text = datetime.strftime(datetime.fromtimestamp(data_base.get_time()[0]), '%d.%H:%M')
                await bot.send_message(m.from_user.id,
                                       "Время закрытия: "
                                       f"{text}",
                                       reply_markup=inline_product_menu.set_time())


@dp.message_handler(text="Скачать счет за сегодня")
async def down_check_menu(m: Message):
    if data_base.get_user(m.from_user.id) is not None:
        if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
            try:
                await bot.send_document(m.from_user.id,
                                        open(f"Data/{datetime.strftime(datetime.today(), '%d.%m.%Y')}.xlsx", "rb"))
            except:
                await bot.send_message(m.from_user.id, "Счет за сегодня не найден")


@dp.message_handler(text="Управление счетами")
async def checks_menu(m: Message):
    try:
        if data_base.get_user(m.from_user.id) is not None:
            if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
                if len(data_base.get_checks()) != 0:
                    await m.answer("Сохраненные счета")
                    users = []
                    for user in data_base.get_checks():
                        if user[0] not in users:
                            users.append(user[0])
                            data_user = data_base.get_user(user[0])
                            text = ''
                            summa = 0
                            books = data_base.get_user_checks(user[0])
                            for book in books:
                                text += f"Книга: {book[1]}\n" \
                                        f"Цена: {book[3]} Рублей\n" \
                                        f"Взято: {book[2]} шт\n" \
                                        f"Общая сумма: {book[3] * book[2]} Рублей\n\n"
                                summa += book[3] * book[2]
                            await bot.send_message(m.from_user.id,
                                                   f"Пользователь: {data_user[2]}(@{data_user[1]})\n"
                                                   f"Город: {data_user[3]}\n"
                                                   f"Телефон: {data_user[4]}\n\n"
                                                   f"{text}"
                                                   f"Итоговая сумма: {summa} Рублей")
                            time.sleep(1)
                    await bot.send_message(m.from_user.id,
                                           "Выберите действие",
                                           reply_markup=inline_product_menu.get_check())
                else:
                    await m.answer("Вы еще не сохраняли счета")
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'checks_menu\n{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_checks_"))
async def call_check(call: CallbackQuery):
    try:
        if call.data == "call_checks_send":
            await call.message.edit_text("Отправлено")
            users = []
            data_users = data_base.get_checks()
            for user in data_users:
                if user[0] not in users:
                    users.append(user[0])
                    text = ''
                    summa = 0
                    books = data_base.get_user_checks(user[0])
                    books_xl = []
                    countes_xl = []
                    prices_xl = []
                    for book in books:
                        books_xl.append(book[1])
                        countes_xl.append(book[2])
                        prices_xl.append(book[3])
                        text += f"Книга: {book[1]}\n" \
                                f"Цена: {book[3]} Рублей\n" \
                                f"Взято: {book[2]} шт\n" \
                                f"Общая сумма: {book[3] * book[2]} Рублей\n\n"
                        summa += book[3] * book[2]
                    user_info = data_base.get_user(user_id=user[0])
                    xl.edit_xl(datetime.strftime(datetime.today(), "%d.%m.%Y"),
                               f"{user_info[2]} (@{user_info[1]})", books_xl, prices_xl, countes_xl, summa)
                    time.sleep(1)
                    xl.edit_total(datetime.strftime(datetime.today(), "%d.%m.%Y"),
                                  data_base.get_user(user[0])[1], summa)
                    time.sleep(1)
                    data_base.delete_check(user[0])
                    await bot.send_message(user[0],
                                           "Доброго времени суток🙂\n"
                                           "Вам выставлен счет по следующим книгам\n\n"
                                           f"{text}"
                                           f"Итоговая сумма: {summa} Рублей\n\n"
                                           "Оплатите в течение суток\n"
                                           "Скриншот чека присылать Алёне (@Alena597)\n"
                                           "Скриншот самого счета после оплаты @knigogolikk")

        elif call.data == "call_checks_change":
            count = math.ceil(len(data_base.get_checks()) / 10)
            await call.message.edit_text("Выберите пользователя\n"
                                         f"Страница 1/{count}",
                                         reply_markup=inline_product_menu.select_user(data_base.get_checks(),
                                                                                      1,
                                                                                      count))
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'call_check\n{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_change"))
async def call_change(call: CallbackQuery):
    user_id = call.data.split('_')[2]
    book = call.data.split('_')[3]
    if book == "0":
        await bot.approve_chat_join_request()
        count = math.ceil(len(data_base.get_user_checks(user_id)) / 10)
        await call.message.edit_text("Выберите книгу\n"
                                     f"Страница 1/{count}",
                                     reply_markup=inline_product_menu.change_book(user_id,
                                                                                  data_base.get_user_checks(user_id),
                                                                                  1,
                                                                                  count))
    else:
        data_base.delete_row_check(user_id, book)
        await call.message.edit_text("Книга удалена со счета⚙️")


@dp.callback_query_handler(Text(startswith="call_time_"))
async def call_time(call: CallbackQuery):
    try:
        if call.data == "call_time_change":
            await bot.delete_message(call.from_user.id,
                                     call.message.message_id)
            await bot.send_message(call.from_user.id,
                                   "Введите новое время в формате Дата.Час:Минута",
                                   reply_markup=reply_menu.cancel_state())
            await states_class.EditBook.time.set()

        elif call.data == "call_time_end":
            await call.message.edit_text("Проверьте книги")
            for book in data_base.get_books():
                await bot.send_message(call.from_user.id,
                                       f"Книга: {book[1]}\n"
                                       f"Количество: {book[2]}\n"
                                       f"Взято: {len(data_base.get_count_order(book[1]))}\n"
                                       f"Цена: {book[3]}")
                time.sleep(1)
            await bot.send_message(call.from_user.id,
                                   "Все верно?",
                                   reply_markup=inline_product_menu.end_choice())
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'call_time\n{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_book"))
async def call_book(call: CallbackQuery):
    try:
        if call.data == "call_book_change":
            count = math.ceil(len(data_base.get_books()) / 10)
            await call.message.edit_text("Выберите книгу\n"
                                         f"Страница 1/{count}",
                                         reply_markup=inline_product_menu.edit_book(data_base.get_books(),
                                                                                    1,
                                                                                    count))
        elif call.data == "call_book_end":
            count = math.ceil(len(data_base.get_books()) / 10)
            await call.message.edit_text("Выберите книгу\n"
                                         f"Страница 1/{count}",
                                         reply_markup=inline_product_menu.select_book(data_base.get_books(),
                                                                                      1,
                                                                                      count))
        elif call.data == "call_books_end":
            await call.message.edit_text("Выставите счета на оплату")
            text = {}
            books = data_base.get_books()
            for book in books:
                for order in data_base.get_book_order(book[1], book[2]):
                    if text.get(order[1]) is None:
                        text.update(
                            {order[1]:
                                 {book[1]:
                                      {'book_name': book[1],
                                       'count': 1,
                                       'price': int(book[3]),
                                       'suma': int(book[3])
                                       }
                                  }
                             }
                        )
                    elif text[order[1]].get(book[1]) is None:
                        text[order[1]].update(
                            {book[1]:
                                 {'book_name': book[1],
                                  'count': 1,
                                  'price': int(book[3]),
                                  'suma': int(book[3])
                                  }
                             }
                        )
                    else:
                        text[order[1]][book[1]].update(
                            {'count': text[order[1]][book[1]]['count'] + 1,
                             'suma': int(book[3]) * int(text[order[1]][book[1]]['count'] + 1)
                             }
                        )
            data_base.end_time()
            for user in text:
                data_user = data_base.get_user(user)
                check = ''
                summa = 0
                for elem in text[user].values():
                    check += f"Книга: {elem['book_name']}\n" \
                             f"Цена: {elem['price']} Рублей\n" \
                             f"Взято: {elem['count']} шт\n" \
                             f"Общая сумма: {elem['suma']} Рублей\n\n"
                    summa += elem['suma']
                await bot.send_message(call.from_user.id,
                                       f"Пользователь: {data_user[2]}(@{data_user[1]})\n"
                                       f"Город: {data_user[3]}\n"
                                       f"Телефон: {data_user[4]}\n")
                await bot.send_message(call.from_user.id,
                                       f"{check}"
                                       f"Итоговая сумма: {summa} Рублей",
                                       reply_markup=inline_product_menu.send_check(data_user[0]))
                time.sleep(1)
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'call_book\n{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_select_"))
async def call_once(call: CallbackQuery):
    try:
        if call.data == "call_select_cancel":
            await call.message.edit_text("Отменено")
        else:
            await call.message.edit_text("Выставите счета на оплату")
            text = {}
            book = data_base.get_book(call.data.split('_')[2])
            for order in data_base.get_book_order(book[1], book[2]):
                if text.get(order[1]) is None:
                    text.update(
                        {order[1]:
                             {book[1]:
                                  {'book_name': book[1],
                                   'count': 1,
                                   'price': int(book[3]),
                                   'suma': int(book[3])
                                   }
                              }
                         }
                    )
                elif text[order[1]].get(book[1]) is None:
                    text[order[1]].update(
                        {book[1]:
                             {'book_name': book[1],
                              'count': 1,
                              'price': int(book[3]),
                              'suma': int(book[3])
                              }
                         }
                    )
                else:
                    text[order[1]][book[1]].update(
                        {'count': text[order[1]][book[1]]['count'] + 1,
                         'suma': int(book[3]) * int(text[order[1]][book[1]]['count'] + 1)
                         }
                    )
            data_base.end_once(book[1])
            for user in text:
                data_user = data_base.get_user(user)
                check = ''
                summa = 0
                for elem in text[user].values():
                    check += f"Книга: {elem['book_name']}\n" \
                             f"Цена: {elem['price']} Рублей\n" \
                             f"Взято: {elem['count']} шт\n" \
                             f"Общая сумма: {elem['suma']} Рублей\n\n"
                    summa += elem['suma']
                await bot.send_message(call.from_user.id,
                                       f"Пользователь: {data_user[2]}(@{data_user[1]})\n"
                                       f"Город: {data_user[3]}\n"
                                       f"Телефон: {data_user[4]}")
                await bot.send_message(call.from_user.id,
                                       f"{check}"
                                       f"Итоговая сумма: {summa} Рублей",
                                       reply_markup=inline_product_menu.send_check(data_user[0]))
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_send_check"))
async def call_send_check(call: CallbackQuery):
    try:
        user_id = call.data.split('_')[3]
        data = call.message.text.split("\n\n")
        books = []
        prices = []
        countes = []
        await call.message.edit_text(f"{call.message.text}\n\n"
                                     "Отправлено✅")
        for text in data:
            if text.split(':')[0] == "Итоговая сумма":
                itog = text.split(' ')[2]
                break
            else:
                text = text.split("\n")
                books.append(text[0].split(':')[1].strip())
                prices.append(text[1].split(' ')[1])
                countes.append(text[2].split(' ')[1])
        user = data_base.get_user(user_id)
        xl.edit_xl(datetime.strftime(datetime.today(), "%d.%m.%Y"),
                   f"{user[2]} @({user[1]})", books, prices, countes, itog)
        xl.edit_total(datetime.strftime(datetime.today(), "%d.%m.%Y"),
                      user[2], itog)
        await bot.send_message(user_id,
                               "Доброго времени суток🙂\n"
                               "Вам выставлен счет по следующим книгам\n\n"
                               f"{call.message.text}\n"
                               "Оплатите в течение суток\n"
                               "Скриншот чека присылать Алёне (@Alena597)\n"
                               "Скриншот самого счета после оплаты @knigogolikk")
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_save_check"))
async def call_save_check(call: CallbackQuery):
    try:
        user_id = call.data.split('_')[3]
        data = call.message.text.split("\n\n")
        await call.message.edit_text(f"{call.message.text}\n\n"
                                     "Сохранено📥")
        for text in data:
            if text.split(':')[0] == "Итоговая сумма":
                break
            else:
                text = text.split("\n")
                data_base.add_check(user_id,
                                    text[0].split(':')[1].strip(),
                                    text[2].split(' ')[1],
                                    text[1].split(' ')[1])
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_edit_"))
async def call_edit(call: CallbackQuery, state: FSMContext):
    await state.update_data(book_name=call.data.split('_')[2])
    await call.message.edit_text("Введите новое количество")
    await states_class.EditBook.count.set()


@dp.callback_query_handler(Text(startswith="call_dist_"))
async def call_dist(call: CallbackQuery):
    try:
        if call.data == "call_dist_yes":
            if data_base.get_time()[0] == 0:
                dt = datetime.today()
                day = datetime.strftime(dt, "%d")
                dt = dt.replace(day=int(day) + 1, hour=0, minute=0)
                data_base.set_time(dt.timestamp())
            await call.message.edit_caption(f"{call.message.md_text}\n\n"
                                            "*Отправлено✅*", parse_mode=ParseMode.MARKDOWN_V2)
            book_name = call.message.caption.split("Ваша книга: ")[1].split('.')[0]
            book_price = call.message.caption.split("Цена: ")[1].split('.')[0]
            book_count = call.message.caption.split("Количество: ")[1].split('.')[0]
            data_base.add_book(book_name, book_count, book_price)
            await bot.send_photo(config.get_config("Settings", "chat"),
                                 photo=call.message.photo[-1].file_id,
                                 caption=f"{book_name}\n"
                                         f"Цена: {book_price}\n"
                                         f"Количество: {book_count} шт.\n",
                                 reply_markup=inline_product_menu.get_no(0, book_count))
        elif call.data == "call_dist_no":
            await call.message.edit_caption(f"{call.message.md_text}\n\n"
                                            "*Отменено❌*", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        error = tr.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
        await bot.send_message(5536543760, f'{e} in {error.lineno} row:{error.line}')


@dp.callback_query_handler(Text(startswith="call_next_"))
async def call_next(call: CallbackQuery):
    data = call.data.split('_')
    if data[2] == "edit":
        count = math.ceil(len(data_base.get_books()) / 10)
        await call.message.edit_text("Выберите книгу\n"
                                     f"Страница {data[3]}/{count}",
                                     reply_markup=inline_product_menu.edit_book(data_base.get_books(),
                                                                                int(data[3]),
                                                                                count))
    elif data[2] == "select":
        count = math.ceil(len(data_base.get_books()) / 10)
        await call.message.edit_text("Выберите книгу\n"
                                     f"Страница {data[3]}/{count}",
                                     reply_markup=inline_product_menu.edit_book(data_base.get_books(),
                                                                                int(data[3]),
                                                                                count))
    elif data[2] == "user":
        count = math.ceil(len(data_base.get_checks()) / 10)
        await call.message.edit_text("Выберите пользователя\n"
                                     f"Страница {data[3]}/{count}",
                                     reply_markup=inline_product_menu.select_user(data_base.get_checks(),
                                                                                  int(data[3]),
                                                                                  count))
    elif data[2] == "change":
        user_id = data[4]
        count = math.ceil(len(data_base.get_user_checks(user_id)) / 10)
        await call.message.edit_text("Выберите книгу\n"
                                     f"Страница {data[3]}/{count}",
                                     reply_markup=inline_product_menu.change_book(user_id,
                                                                                  data_base.get_user_checks(user_id),
                                                                                  int(data[3]),
                                                                                  count))


@dp.message_handler(text="Найти пользователей")
async def add_book_menu(m: Message):
    if data_base.get_user(m.from_user.id) is not None:
        if str(m.from_user.id) in config.get_config("Settings", "main_admin"):
            await bot.send_message(m.from_user.id, "Введите имя пользователя или его username",
                                   reply_markup=reply_menu.cancel_state())
            await states_class.FindUser.user.set()
