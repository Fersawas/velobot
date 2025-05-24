import pytest
from unittest.mock import AsyncMock, patch

from aiogram.types import Message, CallbackQuery, User, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from handlers import admin_order_router
from handlers.admin import creation

from keyboards.admin_keyboards import (
    start_admin_keyboard,
)

from constants.constants import ADMIN_MESSAGES, MESSAGES


@pytest.mark.asyncio
async def test_start_admin_panel():
    message = AsyncMock()
    state = AsyncMock()
    await admin_order_router.start_admin_panel(message, state)
    message.answer.assert_called_with(
        ADMIN_MESSAGES["start"], reply_markup=start_admin_keyboard
    )


@pytest.mark.asyncio
async def test_back_to_admin():
    callback = AsyncMock()
    callback.message = AsyncMock()

    state = AsyncMock(spec=FSMContext)
    state.clear = AsyncMock()

    await admin_order_router.back_to_admin(callback, state)

    state.clear.assert_called_once()
    callback.message.edit_text.assert_called_once_with(
        ADMIN_MESSAGES["start"], reply_markup=start_admin_keyboard
    )


@pytest.mark.asyncio
async def test_deafult_message():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)

    await admin_order_router.default_message_handler(message, state)

    message.answer.assert_called_once_with(MESSAGES["unknown_command"])


@pytest.mark.asyncio
async def test_start_admin_create():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = "add_admin"
    callback.message = AsyncMock()
    callback.answer = AsyncMock()
    state = AsyncMock(spec=FSMContext)
    state.set_state = AsyncMock()

    await creation.add_admin_start(callback, state)

    state.set_state.assert_called_once_with(creation.AdminCreate.username)
    callback.message.edit_text.assert_called_once_with(
        ADMIN_MESSAGES["admin_username"], reply_markup=creation.cancel_keyboard
    )
    callback.answer.assert_called_once()


@pytest.mark.asyncio
async def test_process_admin_username():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    message.text = "admin"

    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.set_state = AsyncMock()

    await creation.process_admin_username(message, state)

    state.set_state.assert_called_once_with(creation.AdminCreate.phone)
    message.answer.assert_any_call(
        ADMIN_MESSAGES["save_admin_username"].format(username="admin")
    )
    message.answer.assert_any_call(
        ADMIN_MESSAGES["admin_phone"], reply_markup=creation.cancel_keyboard
    )


@pytest.mark.asyncio
async def test_process_admin_username_with_phone():
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    message.text = "admin"

    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={"phone": "12345678901"})
    state.set_state = AsyncMock()

    await creation.process_admin_username(message, state)

    state.set_state.assert_called_once_with(creation.AdminCreate.confirm)
    message.answer.assert_any_call(
        ADMIN_MESSAGES["create_admin"].format(username="admin", phone="12345678901"),
        reply_markup=creation.create_edit_admin,
    )
