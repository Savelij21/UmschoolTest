

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsLoggedIn(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [514557574]




