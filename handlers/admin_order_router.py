import logging

from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from filters.filters import InitAdmin, IsAdmin

from keyboards.admin_keyboards import (
    start_admin_keyboard,
)

from constants.constants import ADMIN_MESSAGES, LOGGER
from handlers.admin.creation import router as creation_router
from handlers.admin.edit import router as edit_router
from handlers.order.main import router as order_router


router = Router()
router.message.filter(or_f(InitAdmin(), IsAdmin()))
router.include_routers(creation_router, edit_router, order_router)
logger = logging.getLogger(__name__)


@router.message(Command("admin"), default_state)
async def start_admin_panel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await state.set_state(None)
        logger.info(LOGGER["clear_state"].format(current_state=current_state))
    await message.answer(ADMIN_MESSAGES["welcome"], reply_markup=ReplyKeyboardRemove())
    await message.answer(ADMIN_MESSAGES["start"], reply_markup=start_admin_keyboard)


@router.callback_query(F.data == "cancel")
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        ADMIN_MESSAGES["start"], reply_markup=start_admin_keyboard
    )
    await callback.answer()
