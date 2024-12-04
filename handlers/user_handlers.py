
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated, Update
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, insert

import asyncio
import logging
import re
from asyncio import Task
from typing import Literal
from datetime import datetime, timedelta

from lexicon.lexicon import LEXICON, QuestionsGroup, Question
# from database.database import AsyncDatabase
# from states.states import TimerStates
# from utils.utils import process_user_on_start, send_start_image, after_start_send_message, cancel_after_start_send_message
from keyboards.keyboards import get_start_kb, get_back_to_start_kb
from filters.user_filters import IsLoggedIn
from utils.utils import answer_for_update
from db.tables import users as users_table


logger = logging.getLogger(__name__)

router = Router()


# /start ----------------------------------------------------------------------------------------------------------
@router.callback_query(F.data == 'start')
@router.message(CommandStart())
async def process_start_command(update: Update, bot: Bot, db_engine: AsyncEngine):
    """
    По команде /start (или кнопке запуска) или по колбэку из сообщения для неавторизованных пользователей
    """
    msg = ('<b>Привет</b> 👋\n\nЭтот бот поможет тебе сохранить свои результаты ЕГЭ 💯,'
           ' чтобы они всегда были у тебя под рукой 👌\n\n'
           'Чтобы воспользоваться функционалом бота 🤖, тебе необходимо <u>войти в свой аккаунт</u>\n\n'
           'Для этого введи команду <b>/main_menu</b> или нажми кнопку ниже 👇\n\n'
           'Если у тебя нет аккаунта, то <u>зарегистрируйся</u> с помощью команды <b>/register</b> '
           'или по кнопке ниже 👇')

    stmt = insert(users_table).values(
        tg_id=update.from_user.id,
        first_name=update.from_user.first_name,
        last_name=update.from_user.last_name
    )

    async with db_engine.connect() as conn:
        await conn.execute(stmt)
        await conn.commit()

    await answer_for_update(update, {
        'text': msg,
        'reply_markup': get_start_kb()
    })

# process register
@router.callback_query(F.data == 'register')
@router.message(Command(commands=['register']))
async def process_register_command(message: Message, state: FSMContext):
    pass


@router.callback_query(~IsLoggedIn())
@router.message(~IsLoggedIn())
async def process_unauthorized_update(update: Update, state: FSMContext):
    """
    Разворот для не авторизованных пользователей
    """
    msg = ('К сожалению, данный функционал доступен только для <u>зарегистрированных</u> пользователей 😔\n\n'
           'Для регистрации введи команду <b>/register</b> или нажми кнопку ниже 👇')

    await answer_for_update(update, {
        'text': msg,
        'reply_markup': get_back_to_start_kb()
    })


@router.callback_query(F.data == 'main_menu', IsLoggedIn())
@router.message(Command(commands=['main_menu']), IsLoggedIn())
async def process_main_menu_command(update: Update, state: FSMContext):
    msg = ('<b>Главное меню</b>\n\n'
           'Здесь ты можешь <u>занести</u> свои баллы ЕГЭ 📝 с помощью команды '
           '<b>/enter_scores</b> или по кнопке ниже 👇\n\n'
           'Если ты уже заносил свои результаты, то можешь <u>посмотреть</u> их 📋 с помощью команды '
           '<b>/view_scores</b> или по кнопке ниже 👇\n\n')

    await answer_for_update(update, {
        'text': msg,
        'reply_markup': None
    })





@router.callback_query(F.data == 'enter_scores')
@router.message(Command(commands=['enter_scores']))
async def process_enter_scores_command(message: Message, state: FSMContext):
    pass


@router.callback_query(F.data == 'view_scores')
@router.message(Command(commands=['view_scores']))
async def process_view_scores_command(message: Message, state: FSMContext):
    pass


