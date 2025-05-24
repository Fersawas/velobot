from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import pandas as pd

from utils.exceptions import WrongNumber, WrongPrice
from db.db_commands import list_admin_names


def clear_phone(phone):
    phone = "".join([char for char in phone if char.isdigit()])
    if len(phone) < 10:
        raise WrongNumber
    return phone


def clear_price(price):
    try:
        price = float(price)
        return price
    except Exception as e:
        raise


async def find_master(master):
    admins = await list_admin_names()
    if not admins:
        return master
    result_master = process.extractOne(master, admins)
    if result_master[1] < 80:
        return master, False
    else:
        return result_master[0], True


def create_excel_orders(orders):
    data = [
        {
            "id": order.id,
            "Название заказа": order.title,
            "Статус заказа": order.status,
            "Стоимость заказа": order.price_estimate,
            "Оплачен": order.is_paid,
            "Клиент": order.fullname,
            "Телефон клиента": order.phone,
            "Мастер": order.master.username if order.master else "Не назначен",
            "Комментарий": order.comment,
        }
        for order in orders
    ]
    df = pd.DataFrame(data)
    df.to_excel("orders_excel/orders.xlsx", index=False)
    return "orders_excel/orders.xlsx"
