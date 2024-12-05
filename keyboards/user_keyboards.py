from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Subject

# general buttons --------------------------------------------------------------------------------------------------
back_to_menu_btn = InlineKeyboardButton(
    text='⬅️ В главное меню',
    callback_data='main_menu'
)


# /start -----------------------------------------------------------------------------------------------------------
def get_start_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Войти',
            callback_data='login'
        ),
        InlineKeyboardButton(
            text='Регистрация',
            callback_data='register'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_back_to_start_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='⬅️ В начало',
            callback_data='start'
        ),
        width=1
    )
    return kb_builder.as_markup()


# main_menu -------------------------------------------------------------------------------------------------------
def get_to_main_menu_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='В главное меню ⬆️',
            callback_data='main_menu'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_main_menu_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Занести баллы 📝',
            callback_data='enter_scores'
        ),
        InlineKeyboardButton(
            text='Посмотреть баллы 📋',
            callback_data='view_scores'
        ),
        width=1
    )
    return kb_builder.as_markup()


# enter_scores ----------------------------------------------------------------------------------------------------
def get_subjects_kb(subjects: List[Subject]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        *[InlineKeyboardButton(
            text=subject.name,
            callback_data=f'subject_{subject.id}'
        ) for subject in subjects],
        width=1
    )
    return kb_builder.as_markup()

