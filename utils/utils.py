from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
