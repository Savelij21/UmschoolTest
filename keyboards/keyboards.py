from typing import List, Tuple, Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON, Guide, QuestionsGroup, Question

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
            callback_data='main_menu'
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


# MENU (as main menu) -----------------------------------------------------------------------------------
def get_menu_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Хочу питание и тренировки  🥣🏃‍♀️',
            callback_data='food_training'
        ),
        InlineKeyboardButton(
            text='Забрать гайд  📃',
            callback_data='guide'
        ),
        InlineKeyboardButton(
            text='Задать вопрос ❓',
            callback_data='question'
        ),
        InlineKeyboardButton(
            text='Хочу на курс  👨‍🏫',
            callback_data='course'
        ),
        width=1
    )
    return kb_builder.as_markup()


# MAIN MENU UPDATES ---------------------------------------------------------------------------------
# question
def get_question_type_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Задать вопрос по курсу 👨‍🏫',
            callback_data='course_questions'
        ),
        InlineKeyboardButton(
            text='Задать вопрос по похудению 🥦',
            callback_data='weight_loss_questions'
        ),
        back_to_menu_btn,
        width=1
    )
    return kb_builder.as_markup()


# course
def get_course_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Информация о курсе',
            url='https://t.me/+z95IeBYsKZg3MGIy'
        ),
        back_to_menu_btn,
        width=1
    )
    return kb_builder.as_markup()


# food training
def get_food_training_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        back_to_menu_btn,
        width=1
    )
    return kb_builder.as_markup()


# guide
def get_guides_list_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    guides: list[Guide] = LEXICON['guides']
    buttons = [
        InlineKeyboardButton(
            text=guide.title,
            url=guide.url
        ) for guide in guides
    ]
    kb_builder.row(
        *buttons,
        back_to_menu_btn,
        width=1
    )
    return kb_builder.as_markup()


# COURSE / WEIGHT LOSS QUESTIONS ----------------------------------------------------------------------------
# Questions list
def get_questions_list_kb(questions_group: QuestionsGroup) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=str(i + 1),
            callback_data=f'{questions_group.callback_data}_{i}'
        ) for i in range(len(questions_group.questions))
    ]
    kb_builder.row(
        *buttons,
        width=3
    )

    if questions_group.callback_data == 'course_questions':
        kb_builder.row(
            InlineKeyboardButton(
                text='К вопросам по похудению 🥦',
                callback_data='weight_loss_questions'
            ),
            width=1
        )
    else:  # if weight_loss_questions
        kb_builder.row(
            InlineKeyboardButton(
                text='К вопросам по курсу 👨‍🏫',
                callback_data='course_questions'
            ),
        )

    kb_builder.row(
        back_to_menu_btn,
        width=1
    )
    return kb_builder.as_markup()


# Question answer
def get_question_kb(question: Question,
                    questions_group: QuestionsGroup,
                    width: int = 1) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text='⬅️ Назад к вопросам',
            callback_data=questions_group.callback_data
        ),
        back_to_menu_btn
    ]

    if question.button is not None:
        buttons.insert(
            0,
            InlineKeyboardButton(
                text=question.button.text,
                url=question.button.url
            )
        )

    kb_builder.row(
        *buttons,
        width=width
    )
    return kb_builder.as_markup()
