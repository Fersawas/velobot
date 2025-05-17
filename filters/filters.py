import os
from aiogram.filters import Filter
from aiogram.types import Message
from db.db_commands import admin_username_get

from dotenv import load_dotenv

load_dotenv()

ADMINS = os.getenv("ADMINS")


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        print("check")
        return await admin_username_get(message.from_user.username)


class InitAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        print("check InitAdmin")
        return message.from_user.username in ADMINS
