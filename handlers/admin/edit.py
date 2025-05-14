import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.db_commands import admin_list, admin_retrieve, admin_edit, admin_remove

from keyboards.admin_keyboards import (
    cancel_keyboard,
    get_admin_msg_buttons,
    back_admins_keyboard,
    change_admin_keyboard,
    re_edit_admin_keyboard,
    confirm_edit_admin_keyboard,
    remove_admin_keyboard,
)
from states.admin_states import AdminEdit
from constants.constants import ADMIN_MESSAGES
from utils.utils import clear_phone
from utils.exceptions import WrongNumber, NotSuchUser


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "edit_admins")
async def start_admin_edit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    admins = await admin_list()
    if not admins:
        await callback.message.answer(
            ADMIN_MESSAGES["no_admins"],
            reply_markup=cancel_keyboard,
        )
        return

    message, keyboard = get_admin_msg_buttons(admins)

    await callback.message.edit_text(
        message,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()
    await state.set_state(AdminEdit.choose_admin)


@router.callback_query(AdminEdit.choose_admin)
async def choose_admin(callback: CallbackQuery, state: FSMContext):
    admin_id = callback.data
    if not admin_id.isdigit():
        await callback.message.edit_text(
            ADMIN_MESSAGES["not_id"], reply_markup=back_admins_keyboard
        )
        return
    try:
        admin = await admin_retrieve(int(admin_id))
        await callback.message.edit_text(
            ADMIN_MESSAGES["admin_retrieve"].format(
                username=admin.username, phone=admin.phone
            ),
            reply_markup=change_admin_keyboard,
            parse_mode="Markdown",
        )
        await callback.answer()
        await state.update_data(selected_admin=admin)
        await state.set_state(AdminEdit.confirm_action)
    except NotSuchUser as e:
        logger.warning(e)
        await callback.message.edit_text(
            ADMIN_MESSAGES["no_such_admin"], reply_markup=back_admins_keyboard
        )
        await callback.answer()


@router.callback_query(F.data == "change_username", AdminEdit.confirm_action)
async def process_username(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["admin_username"], reply_markup=back_admins_keyboard
    )
    await state.set_state(AdminEdit.new_username)
    await callback.answer()


@router.message(AdminEdit.new_username)
async def change_username(message: Message, state: FSMContext):
    new_username = message.text.strip()
    if not new_username:
        await message.answer(ADMIN_MESSAGES["empty_username"])
        return
    await state.update_data(new_username=new_username)
    data = await state.get_data()
    current_admin = data["selected_admin"]
    final_phone = data.get("new_phone") or current_admin.phone
    await state.set_state(AdminEdit.confirm)
    await message.answer(
        ADMIN_MESSAGES["confirm_changes"].format(
            username=new_username,
            phone=final_phone,
        ),
        reply_markup=confirm_edit_admin_keyboard,
    )


@router.callback_query(F.data == "change_phone", AdminEdit.confirm_action)
async def process_phone(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["admin_phone"], reply_markup=back_admins_keyboard
    )
    await state.set_state(AdminEdit.new_phone)
    await callback.answer()


@router.message(AdminEdit.new_phone)
async def change_phone(message: Message, state: FSMContext):
    try:
        new_phone = clear_phone(message.text.strip())
    except WrongNumber as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_number"], reply_markup=cancel_keyboard
        )
        return
    await state.update_data(new_phone=new_phone)
    data = await state.get_data()
    current_admin = data["selected_admin"]
    final_username = data.get("new_username") or current_admin.username
    await message.answer(
        ADMIN_MESSAGES["confirm_changes"].format(
            username=final_username,
            phone=new_phone,
        ),
        reply_markup=confirm_edit_admin_keyboard,
    )
    await state.set_state(AdminEdit.confirm)


@router.callback_query(F.data == "remove_admin", AdminEdit.confirm_action)
async def remove_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_admin = data["selected_admin"]
    await callback.message.edit_text(
        ADMIN_MESSAGES["remove_admin"].format(
            username=current_admin.username, phone=current_admin.phone
        ),
        reply_markup=remove_admin_keyboard,
        parse_mode="Markdown",
    )
    await state.set_state(AdminEdit.delete_admin)


@router.callback_query(F.data == "confirm_delete_admin", AdminEdit.delete_admin)
async def confirm_remove_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_admin = data["selected_admin"]
    success = await admin_remove(current_admin.id)
    if not success:
        await callback.message.edit_text(
            ADMIN_MESSAGES["admin_creation_failed"],
            reply_markup=cancel_keyboard,
            parse_mode="Markdown",
        )
    await state.clear()
    await callback.message.edit_text(
        ADMIN_MESSAGES["removed_admin"], reply_markup=cancel_keyboard
    )


@router.callback_query(F.data == "confirm_changes", AdminEdit.confirm)
async def change_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_admin = data.get("selected_admin")
    admin_id = int(current_admin.id)
    final_phone = data.get("new_phone") or current_admin.phone
    final_username = data.get("new_username") or current_admin.username
    success = await admin_edit(
        admin_id=admin_id, new_username=final_username, new_phone=final_phone
    )
    if not success:
        await callback.message.edit_text(
            ADMIN_MESSAGES["admin_creation_failed"], reply_markup=cancel_keyboard
        )
    await callback.message.edit_text(
        ADMIN_MESSAGES["admin_updated"], reply_markup=cancel_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "re_edit_admin", AdminEdit.confirm)
async def edit_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["edit_choose"], reply_markup=re_edit_admin_keyboard
    )
    await state.set_state(AdminEdit.confirm_action)
    await callback.answer()
