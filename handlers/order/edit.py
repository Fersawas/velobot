import logging
from pprint import pprint

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.order_keyboards import (
    back_to_order_keyboard,
    search_keyboard,
    order_edit_keyboard,
    order_paid_edit_keyboard,
    order_edit_confirm_keyboard,
    photo_edit_keyboard,
    get_msater_msg_buttons,
    get_order_msg_buttons,
)
from states.order_states import OrderEdit
from db.db_commands import (
    get_order_by_id,
    admin_list,
    admin_retrieve,
    get_order_by_master,
    edit_order_db,
)
from db.models import Order

from utils.utils import clear_phone, clear_price

from constants.constants import ADMIN_MESSAGES
from utils.exceptions import OrderDoesNotExists, WrongNumber


router = Router()
logger = logging.getLogger(__name__)


async def process_order_by_id(
    state: FSMContext,
    order_id: str,
    message: Message | None = None,
    callback: CallbackQuery | None = None,
):
    custom_answer = message.answer if message else callback.message.edit_text
    try:
        if not order_id or not order_id.isdigit():
            await custom_answer(
                ADMIN_MESSAGES["no_order_id"], reply_markup=back_to_order_keyboard
            )
            return
        else:
            order = await get_order_by_id(int(order_id))
            await state.update_data(order=order)
            if order.master is None:
                master = "Не назначен"
            else:
                master = order.master.username
            order_message = ADMIN_MESSAGES["order"].format(
                order_id=order.id,
                title=order.title,
                description=order.description,
                model_type=order.model_type,
                price_estimate=order.price_estimate,
                is_paid="Оплачен" if order.is_paid else "Не оплачен",
                fullname=order.fullname,
                phone=order.phone,
                master=master,
                comment=order.comment,
            )
            edit_message = ADMIN_MESSAGES["choose_edit"]
            final_message = order_message + edit_message
            await custom_answer(
                final_message, reply_markup=order_edit_keyboard, parse_mode="Markdown"
            )
            await state.set_state(OrderEdit.get_order)
    except OrderDoesNotExists as e:
        await custom_answer(
            ADMIN_MESSAGES["wrong_order"], reply_markup=back_to_order_keyboard
        )
        return


@router.callback_query(F.data == "edit_order")
async def process_edit_order(callback: CallbackQuery):
    await callback.message.edit_text(
        ADMIN_MESSAGES["order_find"], reply_markup=search_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "order_by_id")
async def process_find_by_order_id(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["order_id_input"])
    await callback.answer()
    await state.set_state(OrderEdit.search_order_id)


@router.message(OrderEdit.search_order_id)
async def find_by_order_id(message: Message, state: FSMContext):
    order_id = message.text.strip()
    await process_order_by_id(message=message, state=state, order_id=order_id)


@router.callback_query(F.data == "orders_by_master")
async def process_find_by_master(callback: CallbackQuery, state: FSMContext):
    admins = await admin_list()
    if not admins:
        await callback.message.answer(
            ADMIN_MESSAGES["no_admins"],
            reply_markup=back_to_order_keyboard,
        )
        return
    masters_message, keyboard = get_msater_msg_buttons(admins)
    await callback.message.edit_text(
        masters_message, reply_markup=keyboard, parse_mode="Markdown"
    )
    await state.set_state(OrderEdit.orders_by_master)


@router.callback_query(OrderEdit.orders_by_master)
async def orders_by_master(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data
    if not master_id.isdigit():
        await callback.message.edit_text(
            ADMIN_MESSAGES["no_master"], reply_markup=back_to_order_keyboard
        )
        return
    try:
        orders = await get_order_by_master(int(master_id))
        if not orders:
            await callback.message.edit_text(
                ADMIN_MESSAGES["empty_orders"], reply_markup=back_to_order_keyboard
            )
        await callback.answer()
    except Exception as e:
        logger.error(e)
        await callback.message.answer(
            ADMIN_MESSAGES["by_master_error"], reply_markup=back_to_order_keyboard
        )
        return
    order_message, keyboard = get_order_msg_buttons(orders)
    await callback.message.edit_text(
        order_message, reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()
    await state.set_state(OrderEdit.get_master_order)


@router.callback_query(OrderEdit.get_master_order)
async def process_order_by_master(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data
    await process_order_by_id(callback=callback, state=state, order_id=order_id)


@router.callback_query(F.data.startswith("order_edit_"), OrderEdit.get_order)
async def process_edit_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace("order_edit_", "")
    await state.update_data(editing_field=field)
    match field:
        case "title":
            await callback.message.edit_text(ADMIN_MESSAGES["new_title"])
            await state.set_state(OrderEdit.edit_field)
        case "description":
            await callback.message.edit_text(ADMIN_MESSAGES["new_description"])
            await state.set_state(OrderEdit.edit_field)
        case "model_type":
            await callback.message.edit_text(ADMIN_MESSAGES["new_model_type"])
            await state.set_state(OrderEdit.edit_field)
        case "price_estimate":
            await callback.message.edit_text(ADMIN_MESSAGES["new_price_estimate"])
            await state.set_state(OrderEdit.edit_field)
        case "is_paid":
            await callback.message.edit_text(
                ADMIN_MESSAGES["new_is_paid"], reply_markup=order_paid_edit_keyboard
            )
            await state.set_state(OrderEdit.callback_edit_field)
            await callback.answer()
        case "fullname":
            await callback.message.edit_text(ADMIN_MESSAGES["new_fullname"])
            await state.set_state(OrderEdit.edit_field)
        case "phone":
            await callback.message.edit_text(ADMIN_MESSAGES["new_phone"])
            await state.set_state(OrderEdit.edit_field)
        case "master":
            print("start master")
            admins = await admin_list()
            if not admins:
                await callback.message.answer(
                    ADMIN_MESSAGES["no_admins"],
                    reply_markup=back_to_order_keyboard,
                )
                return
            masters_message, keyboard = get_msater_msg_buttons(admins)
            await callback.message.edit_text(
                masters_message, reply_markup=keyboard, parse_mode="Markdown"
            )
            print("set state")
            await state.set_state(OrderEdit.callback_edit_field)
            await callback.answer()
        case "comment":
            await callback.message.edit_text(ADMIN_MESSAGES["new_comment"])
            await state.set_state(OrderEdit.edit_field)
        case "photo":
            # photo show
            # await db show photos
            await callback.message.edit_text(
                ADMIN_MESSAGES["photo_start"], reply_markup=photo_edit_keyboard
            )
            await state.set_state(OrderEdit.photo_edit)
        case _:
            pass
    await callback.answer()


@router.message(OrderEdit.edit_field)
async def edit_order_field(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("editing_field")
    order = data.get("order")
    updated_data = {}
    value = message.text.strip()
    if not value:
        await message.answer(
            ADMIN_MESSAGES["empty_edited_field"], reply_markup=back_to_order_keyboard
        )
        return
    match field:
        case "title":
            await state.update_data(title=value)
        case "description":
            await state.update_data(description=value)
        case "model_type":
            await state.update_data(model_type=value)
        case "price_estimate":
            try:
                price_estimate = clear_price(value)
            except Exception as e:
                logger.warning(e)
                await message.answer(
                    ADMIN_MESSAGES["wrong_order_price"],
                    reply_markup=back_to_order_keyboard,
                )
                return
            await state.update_data(price_estimate=price_estimate)
        case "is_paid" | "master":
            pass
        case "fullname":
            await state.update_data(fullname=value)
        case "phone":
            try:
                phone = clear_phone(value)
            except WrongNumber as e:
                logger.warning(e)
                await message.answer(
                    ADMIN_MESSAGES["wrong_number"], reply_markup=back_to_order_keyboard
                )
                return
            await state.update_data(phone=phone)
        case "comment":
            await state.update_data(comment=value)
        case _:
            await message.answer(
                ADMIN_MESSAGES["no_edit_field"], reply_markup=back_to_order_keyboard
            )
    data = await state.get_data()
    master = (
        data.get("master").username
        if data.get("username")
        else order.master.username if order.master else "Не назначен"
    )
    await message.answer(
        ADMIN_MESSAGES["order"].format(
            order_id=order.id,
            title=data.get("title", order.title),
            description=data.get("description", order.description),
            model_type=data.get("model_type", order.model_type),
            price_estimate=data.get("price_estimate", order.price_estimate),
            is_paid="Оплачен" if data.get("is_paid", order.is_paid) else "Не оплачен",
            fullname=data.get("fullname", order.fullname),
            phone=data.get("phone", order.phone),
            master=master,
            comment=data.get("comment", order.comment),
        ),
        reply_markup=order_edit_confirm_keyboard,
        parse_mode="Markdown",
    )
    await state.set_state(OrderEdit.confirm_edit)
    await state.update_data(**updated_data)
    new_data = await state.get_data()
    pprint(new_data)


@router.callback_query(F.data == "confirm_edit_order", OrderEdit.confirm_edit)
async def confirm_order_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order = data.get("order")
    master_id = (
        data.get("master_id")
        if data.get("master_id")
        else order.master.id if order.master else None
    )
    success = await edit_order_db(
        order_id=order.id,
        title=data.get("title", order.title),
        description=data.get("description", order.description),
        model_type=data.get("model_type", order.model_type),
        price_estimate=data.get("price_estimate", order.price_estimate),
        is_paid=data.get("is_paid", order.is_paid),
        fullname=data.get("fullname", order.fullname),
        phone=data.get("phone", order.phone),
        master_id=master_id,
        comment=data.get("comment", order.comment),
    )
    if not success:
        await callback.message.answer(
            ADMIN_MESSAGES["edit_order_error"], reply_markup=back_to_order_keyboard
        )
        await callback.answer()
        return
    else:
        await callback.message.answer(
            ADMIN_MESSAGES["edit_order_success"], reply_markup=back_to_order_keyboard
        )
        await state.clear()
        await callback.answer()


@router.callback_query(OrderEdit.callback_edit_field)
async def edit_order_callback_field(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip()
    print(callback_data)
    match callback_data:
        case "is_paid_edit_true":
            await state.update_data(is_paid=True)
        case "is_paid_edit_false":
            await state.update_data(is_paid=False)
        case _ if callback_data.isdigit():
            master = await admin_retrieve(int(callback_data))
            await state.update_data(master_id=int(master.id), master=master)
        case _:
            await callback.message.edit_text(
                ADMIN_MESSAGES["no_edit_field"], reply_markup=back_to_order_keyboard
            )
            await callback.answer()
            return
    data = await state.get_data()
    order = data.get("order")
    master = (
        data.get("master").username
        if data.get("username")
        else order.master.username if order.master else "Не назначен"
    )
    await callback.message.edit_text(
        ADMIN_MESSAGES["order"].format(
            order_id=order.id,
            title=data.get("title", order.title),
            description=data.get("description", order.description),
            model_type=data.get("model_type", order.model_type),
            price_estimate=data.get("price_estimate", order.price_estimate),
            is_paid="Оплачен" if data.get("is_paid", order.is_paid) else "Не оплачен",
            fullname=data.get("fullname", order.fullname),
            phone=data.get("phone", order.phone),
            master=master,
            comment=data.get("comment", order.comment),
        ),
        reply_markup=order_edit_confirm_keyboard,
        parse_mode="Markdown",
    )
    await state.set_state(OrderEdit.confirm_edit)


@router.callback_query(F.data == "re_edit_order", OrderEdit.confirm_edit)
async def process_re_edit_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order = data.get("order")
    order_message = ADMIN_MESSAGES["order"].format(
        order_id=order.id,
        title=data.get("title", order.title),
        description=data.get("description", order.description),
        model_type=data.get("model_type", order.model_type),
        price_estimate=data.get("price_estimate", order.price_estimate),
        is_paid="Оплачен" if data.get("is_paid", order.is_paid) else "Не оплачен",
        fullname=data.get("fullname", order.fullname),
        phone=data.get("phone", order.phone),
        master=(
            data.get("master").username if data.get("master") else order.master.username
        ),
        comment=data.get("comment", order.comment),
    )
    edit_message = ADMIN_MESSAGES["choose_edit"]
    final_message = order_message + edit_message
    await callback.message.edit_text(
        final_message,
        reply_markup=order_edit_keyboard,
        parse_mode="Markdown",
    )
    await state.set_state(OrderEdit.get_order)
    await callback.answer()
