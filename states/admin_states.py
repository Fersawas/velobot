from aiogram.fsm.state import State, StatesGroup


class AdminCreate(StatesGroup):
    telegram_username = State()
    username = State()
    phone = State()
    confirm = State()


class AdminEdit(StatesGroup):
    choose_admin = State()
    new_username = State()
    new_telegram_username = State()
    new_phone = State()
    confirm_action = State()
    confirm = State()
    delete_admin = State()
