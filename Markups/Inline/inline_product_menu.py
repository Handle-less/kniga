from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Data.data_base import get_count_order, get_user


def dist_book():
    kb = InlineKeyboardMarkup(row_width=2)

    but1 = InlineKeyboardButton("Опубликовать", callback_data="call_dist_yes")
    but2 = InlineKeyboardButton("Отмена", callback_data="call_dist_no")
    kb.row(but1, but2)
    return kb


def get_no(count, total):
    kb = InlineKeyboardMarkup(row_width=1)
    if int(total) > count:
        text = f"Беру ({count} взяли)"
    else:
        text = f"Забронировать (взяли {count})"
    but1 = InlineKeyboardButton(text, callback_data=f"call_get_yes_{count}")
    but2 = InlineKeyboardButton("Отмена", callback_data=f"call_get_no")
    kb.add(but1, but2)
    return kb


def set_time():
    kb = InlineKeyboardMarkup(row_width=2)

    but1 = InlineKeyboardButton("Изменить время", callback_data="call_time_change")
    but2 = InlineKeyboardButton("Закончить бронь", callback_data="call_time_end")
    kb.row(but1, but2)
    return kb


def end_choice():
    kb = InlineKeyboardMarkup(row_width=2)

    but1 = InlineKeyboardButton("Закрыть одну книгу", callback_data="call_book_end")
    but2 = InlineKeyboardButton("Закрыть все книги", callback_data="call_books_end")
    but3 = InlineKeyboardButton("Изменить книгу", callback_data="call_book_change")

    kb.row(but1, but2).add(but3)
    return kb


def edit_book(books, count, total):
    kb = InlineKeyboardMarkup(row_width=2)
    first = (count - 1) * 10
    last = count * 10
    but1 = InlineKeyboardButton(f"{count - 1} стр ⬅", callback_data=f"call_next_edit_{count - 1}")
    but2 = InlineKeyboardButton(f"{count + 1} стр ➡", callback_data=f"call_next_edit_{count + 1}")
    but3 = InlineKeyboardButton("Отмена", callback_data="call_select_cancel")
    for book in books[first:last]:
        kb.row(InlineKeyboardButton(f"{book[1]} {book[2]} штук", callback_data=f"call_edit_{book[0]}"))
    if count - 1 > 0 and total - (count + 1) >= 0:
        kb.row(but1, but2, but3)
    elif count - 1 > 0:
        kb.row(but1, but3)
    elif total - (count + 1) >= 0:
        kb.row(but3, but2)

    return kb


def select_book(books, count, total):
    kb = InlineKeyboardMarkup()
    first = (count - 1) * 10
    last = count * 10
    but1 = InlineKeyboardButton(f"{count - 1} стр ⬅", callback_data=f"call_next_select_{count - 1}")
    but2 = InlineKeyboardButton(f"{count + 1} стр ➡", callback_data=f"call_next_select_{count + 1}")
    but3 = InlineKeyboardButton("Отмена", callback_data="call_select_cancel")

    for book in books[first:last]:
        kb.add(InlineKeyboardButton(f"{book[1]} взяли {len(get_count_order(book[1]))}",
                                    callback_data=f"call_select_{book[1]}"))

    if count - 1 > 0 and total - (count + 1) >= 0:
        kb.row(but1, but2, but3)
    elif count - 1 > 0:
        kb.row(but1, but3)
    elif total - (count + 1) >= 0:
        kb.row(but3, but2)

    return kb


def send_check(user_id):
    kb = InlineKeyboardMarkup(row_width=2)

    but1 = InlineKeyboardButton("Выслать счет", callback_data=f"call_send_check_{user_id}")
    but2 = InlineKeyboardButton("Сохранить счет", callback_data=f"call_save_check_{user_id}")
    kb.row(but1, but2)
    return kb


def get_check():
    kb = InlineKeyboardMarkup(row_width=2)

    but1 = InlineKeyboardButton("Выслать счета", callback_data="call_checks_send")
    but2 = InlineKeyboardButton("Изменить счет", callback_data="call_checks_change")
    kb.row(but1, but2)
    return kb


def select_user(users, count, total):
    kb = InlineKeyboardMarkup(row_width=1)
    users_ = []
    first = (count - 1) * 10
    last = count * 10

    but1 = InlineKeyboardButton(f"{count - 1} стр ⬅", callback_data=f"call_next_user_{count - 1}")
    but2 = InlineKeyboardButton(f"{count + 1} стр ➡", callback_data=f"call_next_user_{count + 1}")
    but3 = InlineKeyboardButton("Отмена", callback_data="call_select_cancel")

    if first != 0:
        for user in users[:first]:
            users_.append(user[0])
    for user in users[first:last]:
        if user[0] not in users_:
            users_.append(user[0])
            data_user = get_user(user[0])
            kb.add(InlineKeyboardButton(f"{data_user[1]}", callback_data=f"call_change_{user[0]}_0"))

    if count - 1 > 0 and total - (count + 1) >= 0:
        kb.row(but1, but2, but3)
    elif count - 1 > 0:
        kb.row(but1, but3)
    elif total - (count + 1) >= 0:
        kb.row(but3, but2)

    return kb


def change_book(user_id, books, count, total):
    kb = InlineKeyboardMarkup(row_width=1)
    books_ = []
    first = (count - 1) * 10
    last = count * 10

    but1 = InlineKeyboardButton(f"{count - 1} стр ⬅", callback_data=f"call_next_change_{count - 1}_{user_id}")
    but2 = InlineKeyboardButton(f"{count + 1} стр ➡", callback_data=f"call_next_change_{count + 1}_{user_id}")
    but3 = InlineKeyboardButton("Отмена", callback_data="call_select_cancel")

    if first != 0:
        for book in books[:first]:
            books_.append(book[1])
    for book in books[first:last]:
        if book[1] not in books_:
            books_.append(book[1])
            kb.add(InlineKeyboardButton(f"{book[1]}", callback_data=f"call_change_{user_id}_{book[1]}"))

    if count - 1 > 0 and total - (count + 1) >= 0:
        kb.row(but1, but2, but3)
    elif count - 1 > 0:
        kb.row(but1, but3)
    elif total - (count + 1) >= 0:
        kb.row(but3, but2)

    return kb
