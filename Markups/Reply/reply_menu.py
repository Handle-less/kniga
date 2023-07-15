from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("Добавить книгу"), "Время бронирования") \
        .row("Скачать счет за сегодня", "Управление счетами") \
        .row("Найти пользователей")

    return kb


def cancel_state():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Отменить⬅"))

    return kb


def share_phone():
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb.add(KeyboardButton("Поделиться номером телефона", request_contact=True))

    return kb
