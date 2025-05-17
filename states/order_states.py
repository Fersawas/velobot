from aiogram.fsm.state import State, StatesGroup


class OrderCreate(StatesGroup):
    title = State()
    description = State()
    model_type = State()
    price_estimate = State()
    is_paid = State()
    fullname = State()
    phone = State()
    master = State()
    comment = State()
    confirm = State()

    title_edit = State()
    description_edit = State()
    model_type_edit = State()
    price_estimate_edit = State()
    is_paid_edit = State()
    fullname_edit = State()
    phone_edit = State()
    master_edit = State()
    comment_edit = State()


class OrderEdit(StatesGroup):
    search_master = State()
    search_order_id = State()

    get_order = State()
    edit_field = State()
    callback_edit_field = State()
    orders_by_master = State()
    get_master_order = State()
    order_select = State()
    confirm_edit = State()

    photo_edit = State()
    add_photo = State()
    delete_photo = State()
    confirm_photo = State()
