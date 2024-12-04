import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, BufferedInputFile, Update
from aiogram.exceptions import TelegramBadRequest

from keyboards.keyboards import get_start_kb
from lexicon.lexicon import LEXICON

from asyncio import Task
import logging
from typing import Dict, Callable


logger = logging.getLogger(__name__)


async def answer_for_update(update: Update, msg_data: Dict[str, Callable | str]):
    if isinstance(update, Message):
        await update.chat.do('typing')
        await update.answer(**msg_data)
    else:
        await update.message.edit_text(**msg_data)



# START PROCESS ------------------------------------------------------------
# user on start
# async def process_user_on_start(message: Message, db: AsyncDatabase) -> bool:
#     user = await db.get_user(message.from_user.id)
#     if not user:
#         await db.add_user(AddToDbUser(
#             tg_id=message.from_user.id,
#             name=message.from_user.username,
#             first_name=message.from_user.first_name,
#             last_name=message.from_user.last_name
#         ))
#         logger.info(f'Пользователь {message.from_user.id}#{message.from_user.username} добавлен в БД')
#         return True  # new user
#     else:
#         logger.info(f'Пользователь {message.from_user.id}#{message.from_user.username} уже есть в БД')
#         # check subscription
#         if user['subscribed']:
#             logger.info(f'Пользователь {message.from_user.id}#{message.from_user.username} подписан')
#         else:
#             await db.subscribe_user(user['tg_id'])
#             logger.info(f'Пользователь {message.from_user.id}#{message.from_user.username} подписан заново')
#         return False  # not new user









