import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from handlers.client_router import router as cl_router
from handlers.admin_order_router import router as ad_router
from middlewares.media_group_middleware import MediaGroupMiddleware

from utils.logger import setup_logger

setup_logger()
load_dotenv()


async def main(TOKEN):
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(cl_router)
    dp.include_router(ad_router)
    dp.message.middleware(MediaGroupMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    print(os.environ.get("BOT_TOKEN"))
    asyncio.run(main(os.environ.get("BOT_TOKEN")))
