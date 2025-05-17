import asyncio
from typing import Callable, Dict, Any, Awaitable
from abc import ABC

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram import types
from aiogram.dispatcher.event.bases import CancelHandler


class MediaGroupMiddleware(BaseMiddleware, ABC):
    media_group: dict = {}

    def __init__(self, latency: int | float = 0.1):
        self.latency = latency
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not hasattr(event, "media_group_id") or not event.media_group_id:
            return await handler(event, data)
        try:
            self.media_group[event.media_group_id].append(event)
            return
        except KeyError:
            self.media_group[event.media_group_id] = [event]
            await asyncio.sleep(self.latency)
            event.model_config["is_last"] = True
            data["album"] = self.media_group[event.media_group_id]

            result = await handler(event, data)

            if event.media_group_id and event.model_config.get("is_last"):
                del self.media_group[event.media_group_id]

            return result
