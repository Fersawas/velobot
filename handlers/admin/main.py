import logging

from aiogram import Router
from aiogram.filters import or_f

from filters.filters import InitAdmin, IsAdmin

from handlers.admin.creation import router as creation_router
from handlers.admin.edit import router as edit_router


router = Router()
router.message.filter(or_f(InitAdmin(), IsAdmin()))
router.include_routers(creation_router, edit_router)
logger = logging.getLogger(__name__)
