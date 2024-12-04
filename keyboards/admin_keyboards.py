
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


back_to_admin_menu_button = InlineKeyboardButton(
    text='⬅️ В админ меню',
    callback_data='admin'
)


def get_back_to_admin_menu_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        back_to_admin_menu_button
    )
    return kb_builder.as_markup()


def get_admin_menu_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Новая рассылка ✉️',
            callback_data='newsletter'
        ),
        InlineKeyboardButton(
            text='Статистика по подписчикам 📊',
            callback_data='subs_stats'
        ),
        InlineKeyboardButton(
            text='Обновить стартовое изображение 🖼',
            callback_data='new_start_image'
        ),
        InlineKeyboardButton(
            text='Резервная копия базы данных 💿',
            callback_data='db_backup'
        ),
        InlineKeyboardButton(
            text='Запланированные задачи ⏰',
            callback_data='scheduler_jobs'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_scheduled_jobs_groups_kb():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Рассылки',
            callback_data='newsletter_jobs'
        ),
        InlineKeyboardButton(
            text='Другие задачи',
            callback_data='other_jobs'
        ),
        back_to_admin_menu_button,
        width=1
    )
    return kb_builder.as_markup()


def get_newsletter_text_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Продолжить',
            callback_data='continue_newsletter_text'
        ),
        InlineKeyboardButton(
            text='Редактировать',
            callback_data='edit_newsletter_text'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_cancel_newsletter_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_newsletter'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_add_newsletter_image_or_not_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Добавить изображение',
            callback_data='add_newsletter_image'
        ),
        InlineKeyboardButton(
            text='Без изображения',
            callback_data='no_newsletter_image'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_finish_newsletter_creation_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Готово к рассылке',
            callback_data='finish_newsletter_creation'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_newsletter'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_start_newsletter_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Запланировать рассылку',
            callback_data='schedule_newsletter'
        ),
        InlineKeyboardButton(
            text='Начать рассылку',
            callback_data='start_newsletter'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_newsletter'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_scheduled_newsletter_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Завершить планирование',
            callback_data='start_newsletter'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_newsletter'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_cancel_new_start_image_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_new_start_image'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_broadcast_process_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='stop_broadcast'
        ),
        width=1
    )
    return kb_builder.as_markup()


def get_confirm_stop_broadcast_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text='Остановить',
            callback_data='confirm_stop_broadcast'
        ),
        InlineKeyboardButton(
            text='Продолжить рассылку',
            callback_data='cancel_stop_broadcast'
        ),
        width=1
    )
    return kb_builder.as_markup()
