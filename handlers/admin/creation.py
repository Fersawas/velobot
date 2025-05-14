import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.db_commands import admin_create
from keyboards.admin_keyboards import (
    start_admin_keyboard,
    create_edit_admin,
    detail_edit_admin,
    cancel_keyboard,
)
from states.admin_states import AdminCreate
from constants.constants import ADMIN_MESSAGES
from utils.utils import clear_phone
from utils.exceptions import WrongNumber


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "add_admin")
async def add_admin_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["admin_username"], reply_markup=cancel_keyboard
    )
    await callback.answer()
    await state.set_state(AdminCreate.username)


@router.message(AdminCreate.username)
async def process_admin_username(message: Message, state: FSMContext):
    username = message.text.strip()
    await state.update_data(username=username)
    data = await state.get_data()
    phone = data.get("phone")
    if phone:
        await state.set_state(AdminCreate.confirm)
        await message.answer(ADMIN_MESSAGES["rename_admin"].format(username=username))
        await message.answer(
            ADMIN_MESSAGES["create_admin"].format(username=username, phone=phone),
            reply_markup=create_edit_admin,
        )

    else:
        await state.set_state(AdminCreate.phone)
        await message.answer(
            ADMIN_MESSAGES["save_admin_username"].format(username=username),
        )
        await message.answer(
            ADMIN_MESSAGES["admin_phone"],
            reply_markup=cancel_keyboard,
        )


@router.message(AdminCreate.phone)
async def process_admin_phone(message: Message, state: FSMContext):
    try:
        phone = clear_phone(message.text.strip())
    except WrongNumber as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_number"], reply_markup=cancel_keyboard
        )
        return
    await state.update_data(phone=phone)
    data = await state.get_data()
    username = data.get("username")
    await message.answer(
        ADMIN_MESSAGES["create_admin"].format(username=username, phone=phone),
        reply_markup=create_edit_admin,
    )
    await state.set_state(AdminCreate.confirm)


@router.callback_query(F.data == "confirm", AdminCreate.confirm)
async def confirm_admin(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    phone = data.get("phone")
    success = await admin_create(username=username, phone=phone)
    if success:
        await callback.message.edit_text(ADMIN_MESSAGES["admin_created"])
    else:
        await callback.message.edit_text(ADMIN_MESSAGES["admin_creation_failed"])
    await callback.message.answer(
        ADMIN_MESSAGES["start"], reply_markup=start_admin_keyboard
    )
    await state.clear()


@router.callback_query(F.data == "edit_admin", AdminCreate.confirm)
async def edit_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["edit_choose"], reply_markup=detail_edit_admin
    )
    await callback.answer()


@router.callback_query(F.data == "edit_username", AdminCreate.confirm)
async def edit_username(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["admin_username"])
    await callback.answer()
    await state.set_state(AdminCreate.username)


@router.callback_query(F.data == "edit_phone", AdminCreate.confirm)
async def edit_phone(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["admin_phone"], reply_markup=cancel_keyboard
    )
    await state.set_state(AdminCreate.phone)
