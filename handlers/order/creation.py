import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.order_states import OrderCreate
from constants.constants import ADMIN_MESSAGES

from db.db_commands import order_create, admin_list, admin_retrieve

from keyboards.order_keyboards import (
    back_to_order_keyboard,
    order_paid_keyboard,
    order_confirm_keyboard,
    start_order_keyboard,
    order_creation_edit_keyboard,
    order_paid_edit_keyboard,
    get_msater_msg_buttons,
)

from utils.utils import clear_price, clear_phone, find_master
from utils.exceptions import WrongNumber, NotSuchUser

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "create_order")
async def create_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["create_order"], reply_markup=back_to_order_keyboard
    )
    await state.set_state(OrderCreate.title)
    await callback.answer()


@router.message(OrderCreate.title)
async def process_order_title(message: Message, state: FSMContext):
    title = message.text.strip()
    await state.update_data(title=title)
    await message.answer(ADMIN_MESSAGES["order_title"].format(title=title))
    await state.set_state(OrderCreate.description)
    await message.answer(
        ADMIN_MESSAGES["create_description"], reply_markup=back_to_order_keyboard
    )


@router.message(OrderCreate.description)
async def process_order_description(message: Message, state: FSMContext):
    description = message.text.strip()
    await state.update_data(description=description)
    await message.answer(
        ADMIN_MESSAGES["order_description"].format(description=description)
    )
    await state.set_state(OrderCreate.model_type)
    await message.answer(
        ADMIN_MESSAGES["create_model_type"], reply_markup=back_to_order_keyboard
    )


@router.message(OrderCreate.model_type)
async def process_order_model_type(message: Message, state: FSMContext):
    model_type = message.text.strip()
    await state.update_data(model_type=model_type)
    await message.answer(
        ADMIN_MESSAGES["order_model_type"].format(model_type=model_type)
    )
    await state.set_state(OrderCreate.price_estimate)
    await message.answer(
        ADMIN_MESSAGES["create_price_estimate"], reply_markup=back_to_order_keyboard
    )


@router.message(OrderCreate.price_estimate)
async def process_order_price_estimate(message: Message, state: FSMContext):
    try:
        price_estimate = clear_price(message.text.strip())
    except Exception as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_order_price"], reply_markup=back_to_order_keyboard
        )
        return
    await state.update_data(price_estimate=price_estimate)
    await message.answer(
        ADMIN_MESSAGES["order_price_estimate"].format(price_estimate=price_estimate)
    )
    await state.set_state(OrderCreate.is_paid)
    await message.answer(
        ADMIN_MESSAGES["create_is_paid"], reply_markup=order_paid_keyboard
    )


@router.callback_query(F.data.startswith("is_paid_"), OrderCreate.is_paid)
async def process_is_paid(callback: CallbackQuery, state: FSMContext):
    if callback.data == "is_paid_true":
        is_paid = True
        message = ADMIN_MESSAGES["order_is_paid_true"]
    elif callback.data == "is_paid_false":
        is_paid = False
        message = ADMIN_MESSAGES["order_is_paid_false"]
    else:
        await callback.message.edit_text(
            ADMIN_MESSAGES["no_is_paid"], reply_markup=order_paid_keyboard
        )
        await callback.answer()
        return
    await state.update_data(is_paid=is_paid)

    await callback.message.edit_text(message)
    await callback.answer()
    await state.set_state(OrderCreate.fullname)
    await callback.message.answer(
        ADMIN_MESSAGES["create_fullname"], reply_markup=back_to_order_keyboard
    )


@router.message(OrderCreate.fullname)
async def process_fullname(message: Message, state: FSMContext):
    fullname = message.text.strip()
    if not fullname:
        await message.answer(
            ADMIN_MESSAGES["no_fullname"], reply_markup=back_to_order_keyboard
        )
        return
    await state.update_data(fullname=fullname)
    await message.answer(ADMIN_MESSAGES["order_fullname"].format(fullname=fullname))
    await state.set_state(OrderCreate.phone)
    await message.answer(
        ADMIN_MESSAGES["create_order_phone"], reply_markup=back_to_order_keyboard
    )


@router.message(OrderCreate.phone)
async def process_phone(message: Message, state: FSMContext):
    try:
        phone = clear_phone(message.text.strip())
    except WrongNumber as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_number"], reply_markup=back_to_order_keyboard
        )
        return
    await state.update_data(phone=phone)
    await message.answer(ADMIN_MESSAGES["order_phone"].format(phone=phone))
    await state.set_state(OrderCreate.master)
    admins = await admin_list()
    if not admins:
        await message.answer(
            ADMIN_MESSAGES["no_admins"],
            reply_markup=back_to_order_keyboard,
        )
        return

    masters_message, keyboard = get_msater_msg_buttons(admins)
    await message.answer(masters_message, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(OrderCreate.master)
async def process_master(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data
    if not master_id.isdigit():
        await callback.message.answer(
            ADMIN_MESSAGES["no_master"], reply_markup=back_to_order_keyboard
        )
        return
    try:
        master = await admin_retrieve(int(master_id))
        await callback.message.answer(
            ADMIN_MESSAGES["order_master"].format(master=master.username)
        )
        await state.update_data(master=master)
        await state.set_state(OrderCreate.comment)
        await callback.message.answer(
            ADMIN_MESSAGES["create_comment"], reply_markup=back_to_order_keyboard
        )
    except NotSuchUser as e:
        logger.warning(e)
        await callback.message.answer(
            ADMIN_MESSAGES["no_such_admin"], reply_markup=back_to_order_keyboard
        )
        await callback.answer()
    await state.update_data(master=master)


@router.message(OrderCreate.comment)
async def procces_comment(message: Message, state: FSMContext):
    comment = message.text.strip() if message.text else None
    if comment:
        await state.update_data(comment=comment)
    data = await state.get_data()
    await message.answer(ADMIN_MESSAGES["order_comment"].format(comment=comment))
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "confirm_order", OrderCreate.confirm)
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    success_order = await order_create(
        title=data.get("title"),
        description=data.get("description"),
        model_type=data.get("model_type"),
        price_estimate=data.get("price_estimate"),
        is_paid=data.get("is_paid"),
        fullname=data.get("fullname"),
        phone=data.get("phone"),
        master=data.get("master"),
        comment=data.get("comment"),
    )
    print(success_order)
    if success_order:
        await callback.message.edit_text(
            ADMIN_MESSAGES["order_confirm"].format(order_id=success_order),
            parse_mode="Markdown",
        )
    else:
        await callback.message.edit_text(ADMIN_MESSAGES["order_creation_failed"])
    await callback.answer()
    await state.clear()
    await callback.message.answer(
        ADMIN_MESSAGES["order_start"], reply_markup=start_order_keyboard
    )


@router.callback_query(F.data == "order_creation_edit", OrderCreate.confirm)
async def choose_oder_creation_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["choose_edit"],
        reply_markup=order_creation_edit_keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "order_creation_edit_title")
async def process_title_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_order"])
    await callback.answer()
    await state.set_state(OrderCreate.title_edit)


@router.message(OrderCreate.title_edit)
async def title_edit(message: Message, state: FSMContext):
    title = message.text.strip()
    await state.update_data(title=title)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_description")
async def process_description_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_description"])
    await callback.answer()
    await state.set_state(OrderCreate.description_edit)


@router.message(OrderCreate.description_edit)
async def description_edit(message: Message, state: FSMContext):
    description = message.text.strip()
    await state.update_data(description=description)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_model_type")
async def process_model_type_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_model_type"])
    await callback.answer()
    await state.set_state(OrderCreate.model_type_edit)


@router.message(OrderCreate.model_type_edit)
async def model_type_edit(message: Message, state: FSMContext):
    model_type = message.text.strip()
    await state.update_data(model_type=model_type)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_price_estimate")
async def process_price_estimate_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_price_estimate"])
    await callback.answer()
    await state.set_state(OrderCreate.price_estimate_edit)


@router.message(OrderCreate.price_estimate_edit)
async def price_estimate_edit(message: Message, state: FSMContext):
    try:
        price_estimate = clear_price(message.text.strip())
    except Exception as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_order_price"], reply_markup=back_to_order_keyboard
        )
        return
    await state.update_data(price_estimate=price_estimate)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_is_paid")
async def process_is_paid_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        ADMIN_MESSAGES["create_is_paid"], reply_markup=order_paid_edit_keyboard
    )
    await callback.answer()
    await state.set_state(OrderCreate.is_paid_edit)


@router.callback_query(F.data.startswith("is_paid_edit_"), OrderCreate.is_paid_edit)
async def price_estimate_edit(callback: CallbackQuery, state: FSMContext):
    if callback.data == "is_paid_edit_true":
        is_paid = True
    elif callback.data == "is_paid_edit_false":
        is_paid = False
    else:
        await callback.message.edit_text(
            ADMIN_MESSAGES["no_is_paid"], reply_markup=order_paid_keyboard
        )
        await callback.answer()
        return
    await state.update_data(is_paid=is_paid)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await callback.message.edit_text(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == "order_creation_edit_fullname")
async def process_fullname_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_fullname"])
    await callback.answer()
    await state.set_state(OrderCreate.fullname_edit)


@router.message(OrderCreate.fullname_edit)
async def fullname_edit(message: Message, state: FSMContext):
    fullname = message.text.strip()
    await state.update_data(fullname=fullname)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_phone")
async def process_phone_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_order_phone"])
    await callback.answer()
    await state.set_state(OrderCreate.phone_edit)


@router.message(OrderCreate.phone_edit)
async def phone_edit(message: Message, state: FSMContext):
    try:
        phone = clear_phone(message.text.strip())
    except WrongNumber as e:
        logger.warning(e)
        await message.answer(
            ADMIN_MESSAGES["wrong_number"], reply_markup=back_to_order_keyboard
        )
        return
    await state.update_data(phone=phone)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "order_creation_edit_master")
async def process_master_edit(callback: CallbackQuery, state: FSMContext):
    admins = await admin_list()
    if not admins:
        await callback.message.answer(
            ADMIN_MESSAGES["no_admins"],
            reply_markup=back_to_order_keyboard,
        )
        return

    masters_message, keyboard = get_msater_msg_buttons(admins)
    await callback.message.answer(
        masters_message, reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()
    await state.set_state(OrderCreate.master_edit)


@router.callback_query(OrderCreate.master_edit)
async def master_edit(callback: Message, state: FSMContext):
    master_id = callback.data
    if not master_id.isdigit():
        await callback.message.answer(
            ADMIN_MESSAGES["no_master"], reply_markup=back_to_order_keyboard
        )
        return
    try:
        master = await admin_retrieve(int(master_id))
        await state.update_data(master=master)
        data = await state.get_data()
        await callback.message.answer(
            ADMIN_MESSAGES["order_info"].format(
                title=data.get("title"),
                description=data.get("description"),
                model_type=data.get("model_type"),
                price_estimate=data.get("price_estimate"),
                is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
                fullname=data.get("fullname"),
                phone=data.get("phone"),
                master=data.get("master").username,
                comment=data.get("comment", "-"),
            ),
            reply_markup=order_confirm_keyboard,
            parse_mode="Markdown",
        )
        await state.set_state(OrderCreate.confirm)
        await callback.answer()
    except NotSuchUser as e:
        print(e)
        logger.warning(e)
        await callback.message.answer(
            ADMIN_MESSAGES["no_such_admin"], reply_markup=back_to_order_keyboard
        )
        await callback.answer()


@router.callback_query(F.data == "order_creation_edit_comment")
async def process_comment_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(ADMIN_MESSAGES["create_comment"])
    await callback.answer()
    await state.set_state(OrderCreate.comment_edit)


@router.message(OrderCreate.comment_edit)
async def master_edit(message: Message, state: FSMContext):
    comment = message.text.strip()
    await state.update_data(comment=comment)
    data = await state.get_data()
    await state.set_state(OrderCreate.confirm)
    await message.answer(
        ADMIN_MESSAGES["order_info"].format(
            title=data.get("title"),
            description=data.get("description"),
            model_type=data.get("model_type"),
            price_estimate=data.get("price_estimate"),
            is_paid="Оплачен" if data.get("is_paid") else "Не оплачен",
            fullname=data.get("fullname"),
            phone=data.get("phone"),
            master=data.get("master").username,
            comment=data.get("comment", "-"),
        ),
        reply_markup=order_confirm_keyboard,
        parse_mode="Markdown",
    )
