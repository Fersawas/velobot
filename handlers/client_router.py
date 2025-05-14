from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.db_commands import (
    user_create,
    user_phone_get,
    user_phone_update,
    order_get_for_client,
)
from db.models import Order

from keyboards.admin_keyboards import phone_keyboard, order_keyboard
from constants.constants import MESSAGES, BUTTONS

from utils.utils import clear_phone


router = Router()


class OrderForm(StatesGroup):
    phone_wait = State()


@router.message(CommandStart())
async def start(message: Message):
    await user_create(
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        user_id=message.from_user.id,
    )
    await message.answer(
        MESSAGES["start"].format(name=message.from_user.first_name),
        reply_markup=order_keyboard,
    )


async def send_orders_to_user(message: Message, orders: list[Order]):
    for order in orders:
        await message.answer(
            MESSAGES["order"].format(
                order_id=order.id,
                title=order.title,
                status=order.status,
                description=order.description,
                expectation_date=order.expectation_date,
            )
        )


@router.message(F.text == BUTTONS["order"])
async def show_order(message: Message, state: FSMContext):
    user_id = message.from_user.id
    phone = await user_phone_get(user_id)
    if phone:
        orders = await order_get_for_client(phone=phone)
        if not orders:
            await message.answer(MESSAGES["no_orders"])
        else:
            await send_orders_to_user(message, orders)
    else:
        await state.set_state(OrderForm.phone_wait)
        await message.answer(MESSAGES["phone_request"], reply_markup=phone_keyboard)


@router.message(OrderForm.phone_wait, F.contact)
async def share_number(message: Message, state: FSMContext):
    contact = message.contact.phone_number
    phone = clear_phone(contact)
    user_id = message.from_user.id
    await user_phone_update(user_id, phone)
    await message.answer(MESSAGES["save_phone"], reply_markup=ReplyKeyboardRemove())
    await message.answer("Сейчас посмотрим заказы", reply_markup=order_keyboard)
    orders = await order_get_for_client(phone=phone)
    if not orders:
        await message.answer(MESSAGES["no_orders"])
    else:
        await send_orders_to_user(message, orders)
    await state.clear()
