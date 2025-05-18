import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from keyboards.order_keyboards import start_order_keyboard

from handlers.order.creation import router as creation_router
from handlers.order.edit import router as edit_router
from handlers.order.send import router as send_router
from constants.constants import ADMIN_MESSAGES, LOGGER


router = Router()
router.include_routers(creation_router, edit_router, send_router)
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "start_orders")
async def start_order_panel(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        logger.info(LOGGER["clear_state"].format(current_state=current_state))
    await state.clear()
    await callback.message.edit_text(
        ADMIN_MESSAGES["order_start"], reply_markup=start_order_keyboard
    )
    await callback.answer()
