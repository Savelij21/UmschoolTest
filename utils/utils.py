
from aiogram.types import Message, Update, InlineKeyboardMarkup

from typing import Dict, Callable


async def answer_for_update(update: Update, text: str, kb: InlineKeyboardMarkup = None) -> None:
    if isinstance(update, Message):
        await update.chat.do('typing')
        await update.answer(text, reply_markup=kb)
    else:
        await update.message.edit_text(text, reply_markup=kb)









