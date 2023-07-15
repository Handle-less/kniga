import time, asyncio
from Data import data_base
from Markups.Inline import inline_product_menu


async def check_time(bot):
    while True:
        await asyncio.sleep(2)
        get_time = data_base.get_time()[0]
        time_now = time.time()
        if int(get_time) == 0 or int(get_time) - int(time_now) > 0:
            pass
        else:
            await bot.send_message(363480784, "Выставите счета на оплату")
            text = {}
            books = data_base.get_books()
            for book in books:
                for order in data_base.get_book_order(book[0], book[1]):
                    if text.get(order[1]) is None:
                        text.update(
                            {order[1]:
                                 {book[0]:
                                      {'book_name': book[0],
                                       'count': 1,
                                       'price': int(book[2]),
                                       'suma': int(book[2])
                                       }
                                  }
                             }
                        )
                    elif text[order[1]].get(book[0]) is None:
                        text[order[1]].update(
                            {book[0]:
                                 {'book_name': book[0],
                                  'count': 1,
                                  'price': int(book[2]),
                                  'suma': int(book[2])
                                  }
                             }
                        )
                    else:
                        text[order[1]][book[0]].update(
                            {'count': text[order[1]][book[0]]['count'] + 1,
                             'suma': int(book[2]) * int(text[order[1]][book[0]]['count'] + 1)
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
                await bot.send_message(363480784,
                                       f"Пользователь: {data_user[2]}(@{data_user[1]})\n")
                await bot.send_message(363480784,
                                       f"{check}"
                                       f"Итоговая сумма: {summa} Рублей",
                                       reply_markup=inline_product_menu.send_check(data_user[0]))
