import logging
from pprint import pprint
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states.order_states import OrderSend
from db.db_commands import (
    get_orders_to_send,
    get_order_with_photos,
    update_order_status,
)
from keyboards.order_keyboards import (
    back_to_order_keyboard,
    send_order_keyboard,
    get_order_msg_buttons,
)

from constants.constants import ADMIN_MESSAGES, ADMIN_BUTTONS, MESSAGES
from utils.utils import clear_phone

logger = logging.getLogger(__name__)

router = Router()
logger = logging.getLogger(__name__)


async def send_message_to_user(bot: Bot, order):
    try:
        await bot.send_message(
            chat_id=order.user_id,
            text=MESSAGES["order_is_ready"].format(
                title=order.title, status=order.status
            ),
        )
        media = [InputMediaPhoto(media=photo) for photo in order.photos[0].photos_list]
        await bot.send_media_group(chat_id=order.user_id, media=media)
        return True
    except Exception as e:
        logger.error(e)
        return False


@router.callback_query(F.data == "send_order")
async def send_order_start(callback: CallbackQuery, state: FSMContext):
    orders = await get_orders_to_send()
    message, keyboard = get_order_msg_buttons(orders)
    await callback.message.edit_text(ADMIN_MESSAGES["send_order_start"])
    await callback.answer()
    await state.set_state(OrderSend.select_order)
    await callback.message.answer(message, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(OrderSend.select_order)
async def get_order_to_send(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.strip()
    order = await get_order_with_photos(order_id=int(order_id))
    if not order:
        await callback.message.edit_text(
            ADMIN_MESSAGES["wrong_order"], reply_markup=back_to_order_keyboard
        )
    await state.update_data(order_id=order_id)
    await state.update_data(order=order)
    media = [InputMediaPhoto(media=photo) for photo in order.photos[0].photos_list]
    await callback.message.answer_media_group(media=media)
    master = order.master.username if order.master else "Не назначен"
    await callback.message.answer(
        ADMIN_MESSAGES["view_order_to_send"].format(
            order_id=order.id,
            title=order.title,
            model_type=order.model_type,
            master=master,
            fullname=order.fullname,
        ),
        reply_markup=send_order_keyboard,
        parse_mode="Markdown",
    )
    await state.set_state(OrderSend.confirm_send)


@router.callback_query(OrderSend.confirm_send)
async def confirm_send_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    callback_data = callback.data.strip()
    match callback_data:
        case "send_order_yes":
            data = await state.get_data()
            order_id = data.get("order_id")
            order = await update_order_status(order_id=int(order_id))
            success = await send_message_to_user(bot=bot, order=order)
            if not success:
                await callback.message.edit_text(
                    ADMIN_MESSAGES["send_error"], reply_markup=back_to_order_keyboard
                )
            else:
                await callback.message.edit_text(
                    ADMIN_MESSAGES["send_order_success"],
                    reply_markup=back_to_order_keyboard,
                )
        case "send_order_no":
            await callback.message.edit_text(
                ADMIN_MESSAGES["dont_send_order"], reply_markup=back_to_order_keyboard
            )
        case _:
            await callback.message.edit_text(
                ADMIN_MESSAGES["send_order_wrong"], reply_markup=send_order_keyboard
            )
            return
    await state.clear()
    await callback.answer()
