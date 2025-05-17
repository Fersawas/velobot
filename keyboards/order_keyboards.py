from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.admin_keyboards import admin_cancel

from constants.constants import ADMIN_MESSAGES, ADMIN_BUTTONS, NUMBERS


create_order = InlineKeyboardButton(
    text=ADMIN_BUTTONS["create_order"], callback_data="create_order"
)

edit_order = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_order"], callback_data="edit_order"
)

find_order = InlineKeyboardButton(
    text=ADMIN_BUTTONS["find_order"], callback_data="find_order"
)

start_order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[create_order, edit_order, find_order], [admin_cancel]]
)

cancel_order_button = InlineKeyboardButton(
    text=ADMIN_BUTTONS["back_to_orders"], callback_data="start_orders"
)

back_to_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_order_button]])


# edit master
def get_msater_msg_buttons(admins):
    message = ADMIN_MESSAGES["choose_admin"]
    buttons = []
    for idx, admin in enumerate(admins, 1):
        message += ADMIN_MESSAGES["view_master"].format(
            admin_id=idx,
            username=admin.username,
        )
        if idx % 3 == 1:
            buttons.append([])

        number = (
            NUMBERS[idx]
            if idx <= 10
            else "".join([NUMBERS[int(numb)] for numb in str(idx)])
        )
        buttons[-1].append(
            InlineKeyboardButton(text=number, callback_data=f"{admin.id}")
        )

    buttons.append([cancel_order_button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return message, keyboard


def get_order_msg_buttons(orders):
    message = ADMIN_MESSAGES["choose_order"]
    buttons = []
    for idx, order in enumerate(orders, 1):
        message += ADMIN_MESSAGES["view_order"].format(
            order_number=idx,
            order_id=order.id,
            title=order.title,
            model_type=order.model_type,
            master=order.master.username,
            fullname=order.fullname,
            phone=order.phone,
        )
        if idx % 3 == 1:
            buttons.append([])

        number = (
            NUMBERS[idx]
            if idx <= 10
            else "".join([NUMBERS[int(numb)] for numb in str(idx)])
        )
        buttons[-1].append(
            InlineKeyboardButton(text=number, callback_data=f"{order.id}")
        )

    buttons.append([cancel_order_button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return message, keyboard


order_paid_true = InlineKeyboardButton(
    text=ADMIN_BUTTONS["is_paid_true"], callback_data="is_paid_true"
)

order_paid_false = InlineKeyboardButton(
    text=ADMIN_BUTTONS["is_paid_false"], callback_data="is_paid_false"
)

order_paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_paid_true, order_paid_false], [cancel_order_button]]
)

order_confirm = InlineKeyboardButton(
    text=ADMIN_BUTTONS["confirm_order"], callback_data="confirm_order"
)

order_creation_edit = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_order"], callback_data="order_creation_edit"
)

order_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_confirm, order_creation_edit, cancel_order_button]]
)

order_create_edit_title = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_title"],
    callback_data="order_creation_edit_title",
)

order_create_edit_description = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_description"],
    callback_data="order_creation_edit_description",
)

order_create_edit_model_type = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_model_type"],
    callback_data="order_creation_edit_model_type",
)

order_create_edit_price_estimate = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_price_estimate"],
    callback_data="order_creation_edit_price_estimate",
)

order_create_edit_is_paid = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_is_paid"],
    callback_data="order_creation_edit_is_paid",
)

order_create_edit_fullname = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_fullname"],
    callback_data="order_creation_edit_fullname",
)

order_creation_edit_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_phone"],
    callback_data="order_creation_edit_phone",
)

order_creation_edit_master = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_master"],
    callback_data="order_creation_edit_master",
)

order_creation_edit_comment = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_comment"],
    callback_data="order_creation_edit_comment",
)


order_creation_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            order_create_edit_title,
            order_create_edit_description,
            order_create_edit_model_type,
        ],
        [
            order_create_edit_price_estimate,
            order_create_edit_is_paid,
            order_create_edit_fullname,
        ],
        [
            order_creation_edit_phone,
            order_creation_edit_master,
            order_creation_edit_comment,
        ],
        [cancel_order_button],
    ]
)

# edit is_paid
order_paid_true = InlineKeyboardButton(
    text=ADMIN_BUTTONS["is_paid_true"], callback_data="is_paid_edit_true"
)

order_paid_false = InlineKeyboardButton(
    text=ADMIN_BUTTONS["is_paid_false"], callback_data="is_paid_edit_false"
)

order_paid_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_paid_true, order_paid_false], [cancel_order_button]]
)


# order search

find_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["find_phone"], callback_data="orders_by_phone"
)

find_master = InlineKeyboardButton(
    text=ADMIN_BUTTONS["find_master"], callback_data="orders_by_master"
)

find_order_id = InlineKeyboardButton(
    text=ADMIN_BUTTONS["find_order_id"], callback_data="order_by_id"
)

search_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[find_order_id, find_master], [cancel_order_button]]
)


# edit keyboard

order_edit_title = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_title"],
    callback_data="order_edit_title",
)

order_edit_description = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_description"],
    callback_data="order_edit_description",
)

order_edit_model_type = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_model_type"],
    callback_data="order_edit_model_type",
)

order_edit_price_estimate = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_price_estimate"],
    callback_data="order_edit_price_estimate",
)

order_edit_is_paid = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_is_paid"],
    callback_data="order_edit_is_paid",
)

order_edit_fullname = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_fullname"],
    callback_data="order_edit_fullname",
)

order_edit_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_phone"],
    callback_data="order_edit_phone",
)

order_edit_master = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_master"],
    callback_data="order_edit_master",
)

order_edit_comment = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_comment"],
    callback_data="order_edit_comment",
)

order_edit_photo = InlineKeyboardButton(
    text=ADMIN_BUTTONS["order_edit_photo"], callback_data="order_edit_photo"
)

order_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            order_edit_title,
            order_edit_description,
            order_edit_model_type,
        ],
        [
            order_edit_price_estimate,
            order_edit_is_paid,
            order_edit_fullname,
        ],
        [
            order_edit_phone,
            order_edit_master,
            order_edit_comment,
        ],
        [order_edit_photo],
        [cancel_order_button],
    ]
)

# confirm edit keyboard

order_edit_confirm = InlineKeyboardButton(
    text=ADMIN_BUTTONS["confirm_order"], callback_data="confirm_edit_order"
)

order_re_edit = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_order"], callback_data="re_edit_order"
)

order_edit_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[order_edit_confirm, order_re_edit, cancel_order_button]]
)

# photo edit keyboard

new_photo_add = InlineKeyboardButton(
    text=ADMIN_BUTTONS["new_photo"], callback_data="new_photo_add"
)

delete_photo = InlineKeyboardButton(
    text=ADMIN_BUTTONS["delete_photo"], callback_data="delete_photo"
)

photo_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[new_photo_add, delete_photo], [cancel_order_button]]
)

save_photo = InlineKeyboardButton(
    text=ADMIN_BUTTONS["photo_yes"], callback_data="save_photo_yes"
)

not_save_photo = InlineKeyboardButton(
    text=ADMIN_BUTTONS["photo_no"], callback_data="save_photo_no"
)


photo_save_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[save_photo, not_save_photo], [cancel_order_button]]
)

# delete photo

delete_photo_yes = InlineKeyboardButton(
    text=ADMIN_BUTTONS["photo_yes"], callback_data="delete_photo_yes"
)

delete_photo_no = InlineKeyboardButton(
    text=ADMIN_BUTTONS["photo_no"], callback_data="delete_photo_no"
)

delete_photo_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[delete_photo_yes, delete_photo_no], [cancel_order_button]]
)
