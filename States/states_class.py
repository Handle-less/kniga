from aiogram.dispatcher.filters.state import StatesGroup, State


class CaptchaState(StatesGroup):
    captcha_num = State()
    city = State()
    phone = State()


class AddBook(StatesGroup):
    name = State()
    price = State()
    count = State()
    photo = State()


class EditBook(StatesGroup):
    count = State()
    time = State()


class FindUser(StatesGroup):
    user = State()