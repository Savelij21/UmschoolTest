
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, Update
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import joinedload

import logging
from typing import List

from keyboards.user_keyboards import get_start_kb, get_back_to_start_kb, get_to_main_menu_kb, get_main_menu_kb, get_subjects_kb
from filters.user_filters import IsLoggedIn
from utils.utils import answer_for_update
from db.models import User, Subject, ExamResult
from states.user_states import RegisterUserStates, EnterScoreStates

logger = logging.getLogger(__name__)

router = Router()


# UNAUTHORIZED ---------------
# /start ----------------------------------------------------------------------------------------------------------
@router.callback_query(F.data == 'start')
@router.message(CommandStart())
async def process_start_command(update: Update, state: FSMContext):
    """
    По команде /start (или кнопке запуска) или по колбэку из сообщения для неавторизованных пользователей
    """
    msg = ('<b>Привет</b> 👋\n\nЭтот бот поможет тебе сохранить свои результаты ЕГЭ 💯,'
           ' чтобы они всегда были у тебя под рукой 👌\n\n'
           'Чтобы воспользоваться функционалом бота 🤖, тебе необходимо <u>войти в свой аккаунт</u>\n\n'
           'Для этого введи команду <b>/main_menu</b> или нажми кнопку ниже 👇\n\n'
           'Если у тебя нет аккаунта, то <u>зарегистрируйся</u> с помощью команды <b>/register</b> '
           'или по кнопке ниже 👇')

    await state.clear()  # Очистка состояний, разлогиниваем

    await answer_for_update(update, msg, get_start_kb())


# login -----------------------------------------------------------------------------------------------
@router.callback_query(F.data == 'login')
@router.message(Command(commands=['login']))
async def process_login_command(update: Update, state: FSMContext, session_maker: async_sessionmaker):
    async with session_maker() as session:
        # Попытка найти пользователя по его tg_id
        user = await session.get(User, update.from_user.id)
        if user is None:
            return await answer_for_update(
                update,
                text='Увы, но твой телеграм аккаунт еще <b>не зарегистрирован</b> в нашей системе 😔\n\n',
                kb=get_back_to_start_kb()
            )

    await state.set_data({
        'is_logged': True,
        'first_name': user.first_name,
        'last_name': user.last_name
    })
    return await answer_for_update(
        update,
        text='Ты успешно авторизован, пользуйся на здоровье 😉',
        kb=get_to_main_menu_kb()
    )


# process register ---------------------------------------------------------------------------------
@router.callback_query(F.data == 'register')
@router.message(Command(commands=['register']))
async def process_register_command(update: Update, state: FSMContext):
    await state.update_data(tg_id=update.from_user.id)
    msg = '<b>Регистрация:</b>\n\nВведи свое <b>имя</b>'
    await state.set_state(RegisterUserStates.first_name_input)
    return await answer_for_update(update, msg)


@router.message(F.text, StateFilter(RegisterUserStates.first_name_input))
async def process_first_name_input(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    msg = '<b>Регистрация:</b>\n\nВведи свою <b>фамилию</b>'
    await state.set_state(RegisterUserStates.last_name_input)
    return await message.answer(msg)


@router.message(F.text, StateFilter(RegisterUserStates.last_name_input))
async def process_last_name_input(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    await state.update_data(last_name=message.text)
    data = await state.get_data()
    # add user to db
    async with session_maker() as session:
        session.add(User(
            tg_id=data['tg_id'],
            first_name=data['first_name'],
            last_name=data['last_name']
        ))
        await session.commit()
    await state.clear()
    # фиксируем в стейте данные зарегистрированного юзера
    await state.set_data({
        'is_logged': True,
        'first_name': data['first_name'],
        'last_name': data['last_name']
    })
    await message.answer(
        text='Регистрация прошла успешно, ты <b>авторизован</b> 🎉',
        reply_markup=get_to_main_menu_kb()
    )


# for unauthorized redirect ---------------------------------------------------------------------------------------
@router.callback_query(~IsLoggedIn())
@router.message(~IsLoggedIn())
async def process_unauthorized_update(update: Update, state: FSMContext):
    """
    Разворот для не авторизованных пользователей
    """
    msg = ('К сожалению, данный функционал доступен только для <u>зарегистрированных</u> пользователей 😔\n\n'
           'Для регистрации введи команду <b>/register</b> или нажми кнопку ниже 👇')

    await answer_for_update(update, msg, get_back_to_start_kb())


# AUTHORIZED ----------------------------------------------------------------------------------------
# --- main menu ---------------------------------------------------------------------------------------
@router.callback_query(F.data == 'main_menu', IsLoggedIn())
@router.message(Command(commands=['main_menu']), IsLoggedIn())
async def process_main_menu_command(update: Update, state: FSMContext):
    data = await state.get_data()
    msg = (f'<b>Главное меню</b> [{data["first_name"]} {data["last_name"]}]\n\n'
           f'Здесь ты можешь <u>занести</u> свои баллы ЕГЭ 📝 с помощью команды '
           f'<b>/enter_scores</b> или по кнопке ниже 👇\n\n'
           f'Если ты уже заносил свои результаты, то можешь <u>посмотреть</u> их 📋 с помощью команды '
           f'<b>/view_scores</b> или по кнопке ниже 👇\n\n')

    await answer_for_update(update, msg, get_main_menu_kb())


# --- process enter scores -----------------------------------------------------------------------------
@router.callback_query(F.data == 'enter_scores', IsLoggedIn())
@router.message(Command(commands=['enter_scores']), IsLoggedIn())
async def process_enter_scores_command(update: Update, state: FSMContext, session_maker: async_sessionmaker):
    async with session_maker() as session:
        result = await session.execute(select(Subject))
        subjects: List[Subject] = list(result.scalars().all())

    await state.set_state(EnterScoreStates.select_subject)
    await answer_for_update(
        update,
        text='Выбери <b>предмет</b> 📚',
        kb=get_subjects_kb(subjects=subjects)
    )


@router.callback_query(EnterScoreStates.select_subject, IsLoggedIn())
async def process_subject_selection(callback: CallbackQuery, state: FSMContext, session_maker: async_sessionmaker):
    await state.update_data(subject_id=callback.data.replace('subject_', ''))

    await state.set_state(EnterScoreStates.score_input)
    await callback.message.edit_text(
        text='Введи свой <b>результат (количество баллов, от 0 до 100)</b> по этому предмету 🔢',
        reply_markup=None
    )


@router.message(EnterScoreStates.score_input, IsLoggedIn())
async def process_score_input(message: Message, state: FSMContext, session_maker: async_sessionmaker):
    try:
        score = int(message.text)
        if score < 0 or score > 100:
            raise ValueError
    except ValueError:
        await message.answer('Пожалуйста, введите число от 0 до 100')
        return

    data = await state.get_data()
    await state.clear()
    await state.set_data({
        'is_logged': True,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
    })

    async with session_maker() as session:
        session.add(ExamResult(
            user_id=message.from_user.id,
            subject_id=int(data['subject_id']),
            score=score
        ))
        await session.commit()

    await message.answer(
        text='Запись прошла успешно, твои результаты сохранены 💾',
        reply_markup=get_to_main_menu_kb()
    )


# view scores ---------------------------------------------------------------------------------------
@router.callback_query(F.data == 'view_scores', IsLoggedIn())
@router.message(Command(commands=['view_scores']), IsLoggedIn())
async def process_view_scores_command(update: Update, state: FSMContext, session_maker: async_sessionmaker):

    async with session_maker() as session:
        result = await session.execute(
            select(ExamResult)
            .options(joinedload(ExamResult.subject))
            .where(ExamResult.user_id == update.from_user.id)
        )
        exam_results: List[ExamResult] = list(result.scalars().all())

    # -- если еще не вводил результаты ранее
    if len(exam_results) == 0:
        return await answer_for_update(
            update,
            text='Ты еще не вводил свои результаты :(',
            kb=get_to_main_menu_kb()
        )

    header = "<b>Твои результаты:</b>\n\n"
    text = "\n".join(
        f"<b>{exam_result.subject.name}</b>: {exam_result.score}" for exam_result in exam_results
    )

    return await answer_for_update(
        update,
        text=header + text,
        kb=get_to_main_menu_kb()
    )
