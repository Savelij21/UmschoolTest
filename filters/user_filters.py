

from aiogram.filters import BaseFilter
from aiogram.types import Message, Update
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker


class IsLoggedIn(BaseFilter):
    async def __call__(self, update: Update, state: FSMContext) -> bool:
        user_data = await state.get_data()
        return user_data.get('is_logged', None)




