from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    commands = [
        # BotCommand(
        #     command='/start',
        #     description='Войти'
        # ),
        # BotCommand(
        #     command='/register',
        #     description='Регистрация'
        # ),
        # BotCommand(
        #     command='/enter_scores',
        #     description='Ввести свои баллы ЕГЭ'
        # ),
        # BotCommand(
        #     command='/view_scores',
        #     description='Посмотреть мои баллы ЕГЭ'
        # ),

    ]

    await bot.set_my_commands(commands)

