from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from datetime import datetime, timedelta


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, interval: int = 5):
        self.limit = limit
        self.interval = interval
        self.user_timestamps = {}
        super().__init__()

    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id
        now = datetime.now()
        
        if user_id not in self.user_timestamps:
            self.user_timestamps[user_id] = []

        # Удаляем старые отметки времени
        self.user_timestamps[user_id] = [
            ts for ts in self.user_timestamps[user_id]
            if now - ts < timedelta(seconds=self.interval)
        ]

        if len(self.user_timestamps[user_id]) >= self.limit:
            await event.answer("Слишком много запросов. Пожалуйста, подождите.")
            return

        self.user_timestamps[user_id].append(now)
        return await handler(event, data)
