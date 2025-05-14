from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from constants.constants import BUTTONS, ADMIN_BUTTONS, ADMIN_MESSAGES, NUMBERS


phone_button = KeyboardButton(text=BUTTONS["upload"], request_contact=True)
phone_keyboard = ReplyKeyboardMarkup(keyboard=[[phone_button]], resize_keyboard=True)

order_button = KeyboardButton(text=BUTTONS["order"])
order_keyboard = ReplyKeyboardMarkup(keyboard=[[order_button]], resize_keyboard=True)

admin_cancel = InlineKeyboardButton(
    text=ADMIN_BUTTONS["cancel"], callback_data="cancel"
)

# base admin
add_admin_button = InlineKeyboardButton(
    text=ADMIN_BUTTONS["add_admin"], callback_data="add_admin"
)
admin_orders = InlineKeyboardButton(
    text=ADMIN_BUTTONS["orders"], callback_data="start_orders"
)

admin_edit = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_admins"], callback_data="edit_admins"
)

start_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[add_admin_button, admin_orders, admin_edit]]
)

# create admin
confirm_creation_admin = InlineKeyboardButton(
    text=ADMIN_BUTTONS["create_admin"], callback_data="confirm"
)
edit_admin = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_admin"], callback_data="edit_admin"
)
create_edit_admin = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_creation_admin, edit_admin, admin_cancel]]
)

# edit admin in creation
edit_username = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_username"], callback_data="edit_username"
)
edit_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_phone"], callback_data="edit_phone"
)
detail_edit_admin = InlineKeyboardMarkup(
    inline_keyboard=[[edit_username, edit_phone, admin_cancel]]
)

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[admin_cancel]])


# edit admin
def get_admin_msg_buttons(admins):
    message = ADMIN_MESSAGES["choose_admin"]
    buttons = []
    for idx, admin in enumerate(admins, 1):
        message += ADMIN_MESSAGES["view_admin"].format(
            admin_id=idx, username=admin.username, phone=admin.phone
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

    buttons.append([admin_cancel])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return message, keyboard


back_to_admins = InlineKeyboardButton(
    text=ADMIN_BUTTONS["back_to_admins"], callback_data="edit_admins"
)

back_admins_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_to_admins]])


change_admin_username = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_username"], callback_data="change_username"
)
change_admin_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_phone"], callback_data="change_phone"
)

remove_admin = InlineKeyboardButton(
    text=ADMIN_BUTTONS["remove_admin"], callback_data="remove_admin"
)

change_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [change_admin_username, change_admin_phone, back_to_admins],
        [remove_admin],
    ]
)

confirm_changes = InlineKeyboardButton(
    text=ADMIN_BUTTONS["create_admin"], callback_data="confirm_changes"
)

re_edit_admin = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_admin"], callback_data="re_edit_admin"
)

confirm_edit_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_changes, re_edit_admin, back_to_admins]]
)
# remove admin
confirm_delte = InlineKeyboardButton(
    text=ADMIN_BUTTONS["remove_admin"], callback_data="confirm_delete_admin"
)

remove_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_delte, back_to_admins]]
)

# reedit admin in edit mode

re_edit_username = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_username"], callback_data="change_username"
)
re_edit_phone = InlineKeyboardButton(
    text=ADMIN_BUTTONS["edit_phone"], callback_data="change_phone"
)
re_edit_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [re_edit_username, re_edit_phone, back_to_admins],
        [
            remove_admin,
        ],
    ]
)
