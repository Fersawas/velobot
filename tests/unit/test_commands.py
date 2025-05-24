import pytest
from unittest.mock import AsyncMock, patch
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, ReplyKeyboardRemove, Contact

from handlers import admin_order_router, client_router

from keyboards.admin_keyboards import (
    start_admin_keyboard,
    order_keyboard,
    phone_keyboard,
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
async def test_start_client_panel():
    message = AsyncMock()
    await client_router.start(message)
    message.answer.assert_called_with(
        MESSAGES["start"].format(name=message.from_user.first_name),
        reply_markup=order_keyboard,
    )


@pytest.mark.asyncio
@patch("handlers.client_router.user_phone_get")
@patch("handlers.client_router.order_get_for_client")
async def test_show_order_no_phone(mock_order_get, mock_user_phone_get):
    mock_user_phone_get.return_value = None
    mock_user = AsyncMock(spec=User)
    mock_user.id = 123456789

    message = AsyncMock(spec=Message)
    message.from_user = mock_user
    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)

    from handlers.client_router import show_order

    await show_order(message, state)

    state.set_state.assert_awaited_once_with(client_router.OrderForm.phone_wait)
    await client_router.show_order(message, state)
    message.answer.assert_called_with(
        MESSAGES["phone_request"], reply_markup=phone_keyboard
    )


@pytest.mark.asyncio
@patch("handlers.client_router.user_phone_get")
@patch("handlers.client_router.order_get_for_client")
async def test_show_order_with_phone(mock_order_get, mock_user_phone_get):
    mock_user_phone_get.return_value = 1234568901
    mock_user = AsyncMock(spec=User)
    mock_user.id = 123456789

    message = AsyncMock(spec=Message)
    message.from_user = mock_user
    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)
    with patch("handlers.client_router.order_get_for_client") as mock_order_get:
        mock_order_get.return_value = []
        await client_router.show_order(message, state)

    message.answer.assert_called_with(MESSAGES["no_orders"])


@pytest.mark.asyncio
@patch("handlers.client_router.user_phone_get")
@patch("handlers.client_router.order_get_for_client")
async def test_show_order_with_phone_and_orders(mock_order_get, mock_user_phone_get):
    mock_user_phone_get.return_value = 1234568901
    mock_user = AsyncMock(spec=User)
    mock_user.id = 123456789

    mock_order = AsyncMock()
    mock_order.id = 1
    mock_order.title = "Test Order"
    mock_order.statut = "Test Status"
    mock_order.description = "Test Description"
    mock_order.expectation_date = "Test Date"

    message = AsyncMock(spec=Message)
    message.from_user = mock_user
    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)
    with patch("handlers.client_router.order_get_for_client") as mock_order_get:
        mock_order_get.return_value = [mock_order]
        await client_router.show_order(message, state)

        await client_router.send_orders_to_user(message, [mock_order])

    message.answer.assert_any_call(
        MESSAGES["order"].format(
            order_id=mock_order.id,
            title=mock_order.title,
            status=mock_order.status,
            description=mock_order.description,
            expectation_date=mock_order.expectation_date,
        )
    )


@pytest.mark.asyncio
@patch("handlers.client_router.clear_phone")
@patch("handlers.client_router.user_phone_update")
@patch("handlers.client_router.order_get_for_client")
async def test_share_number(mock_order_get, mock_user_phone_update, mock_clear_phone):
    mock_user = AsyncMock(spec=User)
    mock_user.id = 123456789
    mock_contact = AsyncMock(spec=Contact)
    mock_contact.phone_number = "12345678901"

    mock_clear_phone.return_value = "12345678901"
    mock_user_phone_update.return_value = True
    mock_order_get.return_value = []

    state = AsyncMock(spec=FSMContext)
    state.clear = AsyncMock()

    message = AsyncMock(spec=Message)
    message.contact = mock_contact
    message.from_user = mock_user
    message.answer = AsyncMock()

    await client_router.share_number(message, state)

    mock_clear_phone.assert_called_with("12345678901")
    mock_user_phone_update.assert_called_with(123456789, "12345678901")
    mock_order_get.assert_called_with(phone="12345678901")

    message.answer.assert_any_call(
        MESSAGES["save_phone"], reply_markup=ReplyKeyboardRemove()
    )
    message.answer.assert_any_call(
        "Сейчас посмотрим заказы", reply_markup=order_keyboard
    )

    state.clear.assert_awaited_once()


@pytest.mark.asyncio
@patch("handlers.client_router.clear_phone")
@patch("handlers.client_router.user_phone_update")
@patch("handlers.client_router.order_get_for_client")
async def test_share_number_with_orders(
    mock_order_get, mock_user_phone_update, mock_clear_phone
):
    mock_user = AsyncMock(spec=User)
    mock_user.id = 123456789
    mock_contact = AsyncMock(spec=Contact)
    mock_contact.phone_number = "12345678901"

    mock_order = AsyncMock()
    mock_order.id = 1
    mock_order.title = "Test Order"
    mock_order.statut = "Test Status"
    mock_order.description = "Test Description"
    mock_order.expectation_date = "Test Date"

    mock_clear_phone.return_value = "12345678901"
    mock_user_phone_update.return_value = True
    mock_order_get.return_value = [mock_order]

    state = AsyncMock(spec=FSMContext)
    state.clear = AsyncMock()

    message = AsyncMock(spec=Message)
    message.contact = mock_contact
    message.from_user = mock_user
    message.answer = AsyncMock()

    await client_router.share_number(message, state)

    mock_clear_phone.assert_called_with("12345678901")
    mock_user_phone_update.assert_called_with(123456789, "12345678901")
    mock_order_get.assert_called_with(phone="12345678901")

    message.answer.assert_any_call(
        MESSAGES["save_phone"], reply_markup=ReplyKeyboardRemove()
    )
    message.answer.assert_any_call(
        "Сейчас посмотрим заказы", reply_markup=order_keyboard
    )

    await client_router.send_orders_to_user(message, [mock_order])
    message.answer.assert_any_call(
        MESSAGES["order"].format(
            order_id=mock_order.id,
            title=mock_order.title,
            status=mock_order.status,
            description=mock_order.description,
            expectation_date=mock_order.expectation_date,
        )
    )
